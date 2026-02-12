import { LatLng } from "leaflet";
import { useRef, useState } from "react";
import { useMapEvents } from "react-leaflet";
import { Place } from "../data/mockPlaces";
import { Search } from "lucide-react";

interface Props {
  onFindPlaces: (places: Place[]) => void;
}

const MapCenterListener = ({ onFindPlaces }: Props) => {
  const [showButton, setShowButton] = useState(false);
  const centerRef = useRef<LatLng | null>(null);

  const map = useMapEvents({
    moveend() {
      centerRef.current = map.getCenter();
      setShowButton(true);
    },
  });

  return (
    <div className="absolute z-[1000] w-full h-full p-4 pointer-events-none flex justify-center items-end">
      {showButton && (
        <button
          className="flex gap-2 items-center bg-white pointer-events-auto py-3 px-4 rounded-full font-bold"
          onClick={() => {
            // const foundPlaces = fetchNearbyPlaces(
            //   centerRef.current?.lat,
            //   centerRef.current?.lng
            // );
            const foundPlaces: Place[] = [];
            setShowButton(false);
            onFindPlaces(foundPlaces);
          }}
        >
          <Search className="text-green-500 w-6 h-6" />
          جستجوی این منطقه
        </button>
      )}
    </div>
  );
};

export default MapCenterListener;
