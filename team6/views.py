from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import uuid
from .models import WikiArticle, WikiCategory, WikiArticleRevision, WikiArticleReports

TEAM_NAME = "team6"

# --- Base views ---
def ping(request):
    return JsonResponse({"team": TEAM_NAME, "ok": True})

def base(request):
    articles = WikiArticle.objects.filter(status='published')
    return render(request, "team6/index.html", {"articles": articles})

# لیست مقالات
class ArticleListView(ListView):
    model = WikiArticle
    template_name = 'team6/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = WikiArticle.objects.filter(status='published')
        q = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        search_type = self.request.GET.get('search_type', 'direct')

        if q:  # جستجوی مستقیم یا معنایی
            if search_type == 'semantic':
                queryset = queryset.filter(
                    Q(title_fa__icontains=q) | 
                    Q(body_fa__icontains=q) |
                    Q(summary__icontains=q)
                ).distinct()
            else:  # جستجوی مستقیم
                queryset = queryset.filter(
                    Q(title_fa__icontains=q) | 
                    Q(body_fa__icontains=q)
                )
        
        if cat:  # فیلتر دسته‌بندی
            queryset = queryset.filter(category__slug=cat)
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = WikiCategory.objects.all()
        return context

# ایجاد مقاله
class ArticleCreateView(CreateView):
    model = WikiArticle
    fields = ['title_fa', 'place_name', 'slug', 'body_fa', 'category', 'summary']
    template_name = 'team6/article_form.html'
    success_url = '/team6/'

    # اضافه کردن چک لاگین در dispatch
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/auth/')  # هدایت به صفحه لاگین سرویس مرکزی
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        article = form.save(commit=False)
        # پر کردن اطلاعات نویسنده و ویرایشگر
        article.author_user_id = self.request.user.id
        article.last_editor_user_id = self.request.user.id
        article.status = 'published'
        if not article.slug:
            # اگر slug وارد نشده بود، می‌تونی یه uuid کوتاه بسازی
            article.slug = str(uuid.uuid4())[:8]
        article.url = f"/team6/article/{article.slug}/"
        article.save()
        form.save_m2m()
        return redirect(self.success_url)

# ویرایش مقاله
def edit_article(request, slug):
    article = get_object_or_404(WikiArticle, slug=slug)
    
    if request.method == "POST":
        # ذخیره نسخه قبلی در تاریخچه
        current_rev = getattr(article, 'current_revision_no', 0) or 0
        
        WikiArticleRevision.objects.create(
            article=article,
            revision_no=current_rev + 1,
            body_fa=article.body_fa,
            change_note=request.POST.get('change_note', 'ویرایش بدون توضیح')
        )
        
        # آپدیت مقاله
        article.title_fa = request.POST.get('title_fa', article.title_fa)
        article.body_fa = request.POST.get('body_fa', article.body_fa)
        article.summary = request.POST.get('summary', article.summary)
        article.current_revision_no = current_rev + 2
        
        if self.request.user.is_authenticated:
            article.last_editor_user_id = self.request.user.id
            
        article.save()
        return redirect('team6:article_detail', slug=article.slug)
    
    return render(request, 'team6/article_form.html', {'article': article})

# گزارش مقاله (با slug)
def report_article(request, slug):
    if not request.user.is_authenticated:
        return redirect('/auth/')
    
    article = get_object_or_404(WikiArticle, slug=slug)
    
    if request.method == "POST":
        reporter_id = request.user.id 
        
        WikiArticleReports.objects.create(
            article=article,
            reporter_user_id=reporter_id,
            report_type=request.POST.get('type', 'other'),
            description=request.POST.get('desc', '')
        )
        return render(request, 'team6/report_success.html', {'article': article})
    
    return render(request, 'team6/article_report.html', {'article': article})

# نمایش نسخه‌ها
def article_revisions(request, slug):
    article = get_object_or_404(WikiArticle, slug=slug)
    revisions = WikiArticleRevision.objects.filter(article=article).order_by('-created_at')
    return render(request, 'team6/article_revisions.html', {
        'article': article, 
        'revisions': revisions
    })

# نمایش جزئیات مقاله
def article_detail(request, slug):
    article = get_object_or_404(WikiArticle, slug=slug)
    
    # افزایش بازدید
    if hasattr(article, 'view_count'):
        article.view_count += 1
        article.save()
    
    return render(request, 'team6/article_detail.html', {'article': article})

# API برای محتوای ویکی
def get_wiki_content(request):
    place_query = request.GET.get('place', None)
    
    if not place_query:
        return JsonResponse({"error": "پارامتر place الزامی است"}, status=400)
    
    # جستجو بر اساس نام مکان یا عنوان
    article = WikiArticle.objects.filter(
        Q(place_name__icontains=place_query) | 
        Q(title_fa__icontains=place_query)
    ).first()

    if not article:
        return JsonResponse({"message": "محتوایی برای این مکان یافت نشد"}, status=404)

    # ساخت خروجی
    data = {
        "id": str(article.id) if hasattr(article, 'id') else str(article.slug),
        "title": article.title_fa,
        "place_name": article.place_name,
        "category": article.category.title_fa if article.category else "",
        "tags": list(article.tags.values_list('title_fa', flat=True)) if hasattr(article, 'tags') else [],
        "summary": article.summary if hasattr(article, 'summary') else "",
        "description": article.body_fa,
        "url": f"/team6/article/{article.slug}/",
        "updated_at": article.updated_at.isoformat() if hasattr(article, 'updated_at') else ""
    }
    
    # اضافه کردن تصویر اگر وجود دارد
    if hasattr(article, 'featured_image_url') and article.featured_image_url:
        data["images"] = [article.featured_image_url]
    
    return JsonResponse(data)