import React, { useEffect, useState } from 'react';
import Map, { Marker, Popup, NavigationControl } from "react-map-gl/maplibre";
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import './App.css';
import { fetchAllLocations } from './api';

const HOME_VIEW_STATE = {
    latitude: 53.55,
    longitude: 10.0,
    zoom: 13
  };

function MapWithList() {
  const [viewState, setViewState] = useState(HOME_VIEW_STATE);
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);

  
  useEffect(() => {
    fetchAllLocations()
      .then(response => {
      console.log('Fetched data with axios:', response.data);
      setLocations(response.data.locations || []);
      })
      .catch(error => console.error("Error fetching locations:", error));
  }, []);

  const handleSelectLocation = (loc) => {
    setViewState({
      ...viewState,
      latitude: loc.latitude,
      longitude: loc.longitude,
      zoom: 14
    });
    setSelectedLocation(loc);
  };

  const handleRecenter = () => {
    setViewState(HOME_VIEW_STATE);
    setSelectedLocation(null);
  };

  return (
    <div className="map-page">
      <div className="location-list">
        <h2>Locations</h2>
        {locations.map((loc, index) => (
          <div
            key={index}
            style={{ marginBottom: '1rem', cursor: 'pointer' }}
            onClick={() => handleSelectLocation(loc)}
          >
            <strong>{loc.name}</strong><br />
            {loc.latitude}, {loc.longitude}
          </div>
        ))}
      </div>

      <div className="map-container">
        <Map
          {...viewState}
          style={{ width: '100%', height: '100%' }}
          mapLib={maplibregl}
          mapStyle="https://api.maptiler.com/maps/streets/style.json?key=I17EgKskE3hO4XBpLxwz"
          onMove={evt => setViewState(evt.viewState)}
        >
          {/* Markers for all locations */}
          {locations.map((loc, index) => (
            <Marker
              key={index}
              latitude={loc.latitude}
              longitude={loc.longitude}
            >
              <div
                onClick={() => setSelectedLocation(loc)}
                style={{
                    width: '12px',
                    height: '12px',
                    borderRadius: '50%',
                    backgroundColor: 'red',
                    cursor: 'pointer'
                  }}
              >
    
              </div>
            </Marker>
          ))}

          {selectedLocation && (
            <Popup
              latitude={selectedLocation.latitude}
              longitude={selectedLocation.longitude}
              onClose={() => setSelectedLocation(null)}
              closeButton={true}
              closeOnClick={false}
              anchor="top"
            >
              {console.log("Selected location:", selectedLocation)}
              <div style={{ color: 'black', width: '150px', height: 'auto' }}>
                <h3 style={{ margin: 0 }}>{selectedLocation.name}</h3>
              </div>
            </Popup>
          )}
          <NavigationControl position="top-left" />
        </Map>

        <div style={{ position: 'absolute', top: 10, right: 10 }}>
          <button onClick={handleRecenter}>
            Recenter
          </button>
        </div>
      </div>
    </div>
  );
}

export default MapWithList;
