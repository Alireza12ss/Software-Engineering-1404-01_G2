import { Heart, MapPin, Star, X } from 'lucide-react';
import { FavoritePlace } from '../services/favoritesService';

interface FavoritesPanelProps {
  favorites: FavoritePlace[];
  onClose: () => void;
  onPlaceClick: (lat: number, lng: number) => void;
  onRemoveFavorite: (placeId: string) => void;
}


export default function FavoritesPanel({
  favorites,
  onClose,
  onPlaceClick,
  onRemoveFavorite,
}: FavoritesPanelProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-h-[80vh] overflow-y-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Heart className="w-7 h-7 text-red-500 fill-current" />
          <h2 className="text-xl font-semibold text-gray-800">علاقه مندی های من</h2>
        </div>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
      </div>

      {favorites.length === 0 ? (
        <div className="text-center py-12">
          <Heart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">هنوز علاقه مندی ندارید</p>
          <p className="text-sm text-gray-400 mt-2">
            مکان ها را به علاقه مندی های خود اضافه کنید تا آنها را اینجا مشاهده کنید
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {favorites.map((favorite) => (
            <div
              key={favorite.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex">
                {favorite.place_image && (
                  <img
                    src={favorite.place_image}
                    alt={favorite.place_name}
                    className="w-24 h-24 object-cover rounded-lg mr-4 flex-shrink-0"
                  />
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-gray-800 truncate">
                      {favorite.place_name}
                    </h3>
                    <button
                      onClick={() => onRemoveFavorite(favorite.place_id)}
                      className="flex-shrink-0 ml-2 text-red-500 hover:text-red-700 transition-colors"
                    >
                      <Heart className="w-5 h-5 fill-current" />
                    </button>
                  </div>

                  <div className="flex items-center text-sm text-gray-600 mb-2">
                    <MapPin className="w-4 h-4 mr-1 flex-shrink-0" />
                    <span className="truncate">{favorite.place_address}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="inline-block px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded capitalize">
                      {favorite.place_category}
                    </span>
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-500 fill-current mr-1" />
                      <span className="text-sm font-medium text-gray-800">
                        {favorite.place_rating}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={() =>
                      onPlaceClick(favorite.latitude, favorite.longitude)
                    }
                    className="mt-3 w-full bg-blue-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                  >
                    View on Map
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
