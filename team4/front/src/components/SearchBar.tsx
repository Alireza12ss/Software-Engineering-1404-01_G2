import { useState } from 'react';
import { Search, X } from 'lucide-react';
import { searchLocation } from '../data/mockRoutes';

interface SearchBarProps {
  onLocationSelect: (lat: number, lng: number, name: string) => void;
}

export default function SearchBar({ onLocationSelect }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<{ name: string; lat: number; lng: number }[]>([]);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = (value: string) => {
    setQuery(value);
    if (value.length > 0) {
      const searchResults = searchLocation(value);
      setResults(searchResults);
      setShowResults(true);
    } else {
      setResults([]);
      setShowResults(false);
    }
  };

  const handleSelect = (result: { name: string; lat: number; lng: number }) => {
    onLocationSelect(result.lat, result.lng, result.name);
    setQuery(result.name);
    setShowResults(false);
  };

  const handleClear = () => {
    setQuery('');
    setResults([]);
    setShowResults(false);
  };

  return (
    <div className="relative w-full">
      <div className="flex items-center w-full px-4 gap-2 border-2 border-gray-300 rounded-lg focus-within:outline-none focus-within:ring-2 focus-within:ring-green-500 focus-within:border-transparent">
        <Search className="transform text-green-500 w-6 h-6" />
        <input
          type="text"
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="جستجوی مکان ها..."
          className="w-full py-3 focus:outline-none"
        />
        {query && (
          <button
            onClick={handleClear}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-6 h-6" />
          </button>
        )}
      </div>

      {showResults && results.length > 0 && (
        <div className="absolute top-full mt-2 w-full bg-white rounded-lg shadow-lg border border-gray-200 max-h-80 overflow-y-auto z-50">
          {results.map((result, index) => (
            <button
              key={index}
              onClick={() => handleSelect(result)}
              className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100 last:border-b-0 transition-colors"
            >
              <div className="flex items-center">
                <Search className="w-4 h-4 text-gray-400 mr-3" />
                <span className="text-gray-800">{result.name}</span>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
