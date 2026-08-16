import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Layers } from 'lucide-react';

const createMarkerIcon = (color, text = "") => {
  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `<div style="background-color: ${color}; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #ffffff; box-shadow: 0 3px 8px rgba(0,0,0,0.5); font-weight: bold; font-size: 11px; color: #ffffff;">${text}</div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -14]
  });
};

function MapFocusController({ selectedSite }) {
  const map = useMap();
  useEffect(() => {
    if (selectedSite && selectedSite.latitude && selectedSite.longitude) {
      map.flyTo([selectedSite.latitude, selectedSite.longitude], 13, { duration: 1.2 });
    }
  }, [selectedSite, map]);
  return null;
}

export default function MapView({
  sites = [],
  hospitals = [],
  selectedSite = null,
  onSelectSite
}) {
  const defaultCenter = [21.1458, 79.0882];
  const [layerVisibility, setLayerVisibility] = useState({
    candidates: true,
    hospitals: true,
    buffers: true
  });

  return (
    <div className="relative w-full h-full rounded-xl overflow-hidden border border-slate-800 shadow-xl bg-slate-900">
      {/* Floating Layer Filter Controls */}
      <div className="absolute top-4 right-4 z-[1000] bg-slate-900/90 backdrop-blur-md p-3 rounded-lg border border-slate-700/80 shadow-2xl text-xs space-y-2">
        <div className="font-bold text-slate-200 flex items-center gap-1.5 pb-1 border-b border-slate-700">
          <Layers className="w-3.5 h-3.5 text-brand-400" />
          <span>GIS Layer Controls</span>
        </div>
        <label className="flex items-center gap-2 text-slate-300 cursor-pointer hover:text-white">
          <input
            type="checkbox"
            checked={layerVisibility.candidates}
            onChange={(e) => setLayerVisibility({ ...layerVisibility, candidates: e.target.checked })}
            className="rounded bg-slate-800 border-slate-600 text-brand-600 focus:ring-0 cursor-pointer"
          />
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
          <span>Candidate Sites</span>
        </label>
        <label className="flex items-center gap-2 text-slate-300 cursor-pointer hover:text-white">
          <input
            type="checkbox"
            checked={layerVisibility.hospitals}
            onChange={(e) => setLayerVisibility({ ...layerVisibility, hospitals: e.target.checked })}
            className="rounded bg-slate-800 border-slate-600 text-brand-600 focus:ring-0 cursor-pointer"
          />
          <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span>
          <span>Existing Hospitals</span>
        </label>
        <label className="flex items-center gap-2 text-slate-300 cursor-pointer hover:text-white">
          <input
            type="checkbox"
            checked={layerVisibility.buffers}
            onChange={(e) => setLayerVisibility({ ...layerVisibility, buffers: e.target.checked })}
            className="rounded bg-slate-800 border-slate-600 text-brand-600 focus:ring-0 cursor-pointer"
          />
          <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 inline-block"></span>
          <span>Service Radii (2/5/10km)</span>
        </label>
      </div>

      <MapContainer
        center={defaultCenter}
        zoom={11}
        scrollWheelZoom={true}
        className="w-full h-full"
      >
        <MapFocusController selectedSite={selectedSite} />
        
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Service Catchment Buffer Zones */}
        {layerVisibility.buffers && selectedSite && (
          <>
            <Circle
              center={[selectedSite.latitude, selectedSite.longitude]}
              radius={2000}
              pathOptions={{ color: '#10b981', fillColor: '#10b981', fillOpacity: 0.2, weight: 2, dashArray: '4, 6' }}
            />
            <Circle
              center={[selectedSite.latitude, selectedSite.longitude]}
              radius={5000}
              pathOptions={{ color: '#3b82f6', fillColor: '#3b82f6', fillOpacity: 0.12, weight: 2, dashArray: '4, 6' }}
            />
            <Circle
              center={[selectedSite.latitude, selectedSite.longitude]}
              radius={10000}
              pathOptions={{ color: '#8b5cf6', fillColor: '#8b5cf6', fillOpacity: 0.05, weight: 1.5 }}
            />
          </>
        )}

        {/* Candidate Siting Markers */}
        {layerVisibility.candidates && sites.map((site) => {
          const isSelected = selectedSite && selectedSite.id === site.id;
          const isEligible = site.scores?.is_eligible;
          const color = !isEligible ? '#e11d48' : isSelected ? '#0284c7' : '#059669';
          const label = !isEligible ? '!' : `${site.scores?.rank ?? ''}`;

          return (
            <Marker
              key={site.id}
              position={[site.latitude, site.longitude]}
              icon={createMarkerIcon(color, label)}
              eventHandlers={{
                click: () => onSelectSite && onSelectSite(site)
              }}
            >
              <Popup>
                <div className="p-1 space-y-2 text-xs">
                  <div className="font-bold text-slate-100 text-sm border-b border-slate-700 pb-1">
                    {site.name}
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-slate-300">
                    <div>
                      <span className="text-slate-400 block">Rank:</span>
                      <span className="font-semibold text-white">#{site.scores?.rank ?? '-'}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block">Score:</span>
                      <span className="font-semibold text-white">{site.scores?.overall_score ?? 0} / 100</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block">Parcel Area:</span>
                      <span>{site.parcel_size_acres} Acres</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block">5km Catchment:</span>
                      <span>{site.population_5km?.toLocaleString() || '0'}</span>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => onSelectSite && onSelectSite(site)}
                    className="w-full mt-2 py-1 px-2 rounded bg-brand-600 hover:bg-brand-500 text-white font-medium text-center block transition-colors"
                  >
                    Select Site
                  </button>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Existing Hospital Infrastructure Markers */}
        {layerVisibility.hospitals && hospitals.map((hosp) => (
          <Marker
            key={hosp.id}
            position={[hosp.latitude, hosp.longitude]}
            icon={createMarkerIcon('#dc2626', 'H')}
          >
            <Popup>
              <div className="p-1 text-xs space-y-1">
                <div className="font-bold text-rose-400">{hosp.name}</div>
                <div className="text-slate-300">Classification: {hosp.type}</div>
                <div className="text-slate-300">Capacity: {hosp.beds} Beds</div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}