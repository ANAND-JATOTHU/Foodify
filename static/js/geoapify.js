/**
 * Geoapify Integration Utilities
 * Provides address autocomplete, GPS location, and map features
 */

class GeoapifyUtils {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.autocompleteInstances = [];
    }

    /**
     * Get user's current GPS location
     * @returns {Promise<{lat: number, lon: number, accuracy: number}>}
     */
    getCurrentLocation() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation is not supported by your browser'));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        lat: position.coords.latitude,
                        lon: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    });
                },
                (error) => {
                    let message = 'Unable to retrieve your location';
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            message = 'Location permission denied. Please enable location services.';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            message = 'Location information is unavailable.';
                            break;
                        case error.TIMEOUT:
                            message = 'Location request timed out.';
                            break;
                    }
                    reject(new Error(message));
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        });
    }

    /**
     * Reverse geocode coordinates to address
     * @param {number} lat - Latitude
     * @param {number} lon - Longitude
     * @returns {Promise<object>} Address object
     */
    async reverseGeocode(lat, lon) {
        const url = `https://api.geoapify.com/v1/geocode/reverse?lat=${lat}&lon=${lon}&apiKey=${this.apiKey}`;

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (data.features && data.features.length > 0) {
                const props = data.features[0].properties;
                return {
                    formatted: props.formatted || '',
                    street: props.street || '',
                    housenumber: props.housenumber || '',
                    city: props.city || '',
                    state: props.state || '',
                    postcode: props.postcode || '',
                    country: props.country || '',
                    lat: lat,
                    lon: lon
                };
            }
            throw new Error('No address found');
        } catch (error) {
            console.error('Reverse geocoding error:', error);
            throw error;
        }
    }

    /**
     * Initialize address autocomplete on an input field
     * @param {string|HTMLElement} inputElement - Input element or selector
     * @param {Function} onSelect - Callback when address is selected
     * @param {object} options - Additional options
     */
    initAutocomplete(inputElement, onSelect, options = {}) {
        const input = typeof inputElement === 'string'
            ? document.querySelector(inputElement)
            : inputElement;

        if (!input) {
            console.error('Input element not found');
            return null;
        }

        // Create suggestions container
        const container = document.createElement('div');
        container.className = 'geoapify-autocomplete-suggestions';
        container.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            max-height: 300px;
            overflow-y: auto;
            background: white;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 1000;
            display: none;
        `;

        // Position input wrapper relatively
        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(container);

        let debounceTimer;
        let currentRequest;

        const fetchSuggestions = async (query) => {
            if (query.length < 3) {
                container.style.display = 'none';
                return;
            }

            // Cancel previous request
            if (currentRequest) {
                currentRequest.abort();
            }

            currentRequest = new AbortController();

            const params = new URLSearchParams({
                text: query,
                apiKey: this.apiKey,
                limit: options.limit || 5,
                ...(options.filter && { filter: options.filter }),
                ...(options.bias && { bias: options.bias })
            });

            try {
                const response = await fetch(
                    `https://api.geoapify.com/v1/geocode/autocomplete?${params}`,
                    { signal: currentRequest.signal }
                );
                const data = await response.json();

                displaySuggestions(data.features || []);
            } catch (error) {
                if (error.name !== 'AbortError') {
                    console.error('Autocomplete error:', error);
                }
            }
        };

        const displaySuggestions = (features) => {
            container.innerHTML = '';

            if (features.length === 0) {
                container.style.display = 'none';
                return;
            }

            features.forEach(feature => {
                const item = document.createElement('div');
                item.className = 'autocomplete-item';
                item.style.cssText = `
                    padding: 12px 16px;
                    cursor: pointer;
                    border-bottom: 1px solid #f0f0f0;
                    transition: background 0.2s;
                `;

                const props = feature.properties;
                item.innerHTML = `
                    <div style="font-weight: 500; color: #1c1c1c;">
                        ${props.address_line1 || props.formatted}
                    </div>
                    ${props.address_line2 ? `
                        <div style="font-size: 13px; color: #686b78; margin-top: 4px;">
                            ${props.address_line2}
                        </div>
                    ` : ''}
                `;

                item.addEventListener('mouseenter', () => {
                    item.style.background = '#f9f9f9';
                });

                item.addEventListener('mouseleave', () => {
                    item.style.background = 'white';
                });

                item.addEventListener('click', () => {
                    const addressData = {
                        formatted: props.formatted,
                        street: props.street || '',
                        housenumber: props.housenumber || '',
                        city: props.city || '',
                        state: props.state || '',
                        postcode: props.postcode || '',
                        country: props.country || '',
                        lat: props.lat,
                        lon: props.lon,
                        address_line1: props.address_line1 || '',
                        address_line2: props.address_line2 || ''
                    };

                    input.value = props.formatted;
                    container.style.display = 'none';

                    if (onSelect) {
                        onSelect(addressData);
                    }
                });

                container.appendChild(item);
            });

            container.style.display = 'block';
        };

        // Input event listener
        input.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                fetchSuggestions(e.target.value);
            }, 300);
        });

        // Close suggestions on outside click
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !container.contains(e.target)) {
                container.style.display = 'none';
            }
        });

        // Store instance for cleanup
        const instance = { input, container };
        this.autocompleteInstances.push(instance);

        return instance;
    }

    /**
     * Cleanup all autocomplete instances
     */
    destroyAll() {
        this.autocompleteInstances.forEach(instance => {
            if (instance.container && instance.container.parentElement) {
                instance.container.parentElement.removeChild(instance.container);
            }
        });
        this.autocompleteInstances = [];
    }

    /**
     * Calculate distance between two coordinates (in kilometers)
     * @param {number} lat1 
     * @param {number} lon1 
     * @param {number} lat2 
     * @param {number} lon2 
     * @returns {number} Distance in kilometers
     */
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Earth's radius in km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }
}

// Initialize global instance when API key is available
let geoapifyUtils;

function initGeoapify(apiKey) {
    if (!apiKey) {
        console.warn('Geoapify API key not provided');
        return null;
    }
    geoapifyUtils = new GeoapifyUtils(apiKey);
    return geoapifyUtils;
}
