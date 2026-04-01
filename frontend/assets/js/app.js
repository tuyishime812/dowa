/**
 * DGT-SOUNDS - Main Application JavaScript
 * Music streaming functionality
 */

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// State Management
const state = {
    currentTrack: null,
    isPlaying: false,
    queue: [],
    queueIndex: -1,
    isShuffle: false,
    repeatMode: 'none', // 'none', 'all', 'one'
    volume: 0.8,
    likedTracks: JSON.parse(localStorage.getItem('likedTracks')) || [],
    recentlyPlayed: JSON.parse(localStorage.getItem('recentlyPlayed')) || [],
    detailQueue: []
};

// DOM Elements
const audioPlayer = document.getElementById('audioPlayer');
const playPauseBtn = document.getElementById('playPauseBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const shuffleBtn = document.getElementById('shuffleBtn');
const repeatBtn = document.getElementById('repeatBtn');
const progressBar = document.getElementById('progressBar');
const progress = document.getElementById('progress');
const currentTimeEl = document.getElementById('currentTime');
const durationEl = document.getElementById('duration');
const volumeSlider = document.getElementById('volumeSlider');
const volumeBtn = document.getElementById('volumeBtn');
const playerTitle = document.getElementById('playerTitle');
const playerArtist = document.getElementById('playerArtist');
const playerCover = document.getElementById('playerCover');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const uploadBtn = document.getElementById('uploadBtn');
const uploadModal = document.getElementById('uploadModal');
const closeModal = document.getElementById('closeModal');
const cancelUpload = document.getElementById('cancelUpload');
const uploadForm = document.getElementById('uploadForm');
const genreFilter = document.getElementById('genreFilter');
const sortFilter = document.getElementById('sortFilter');

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadFeaturedTracks();
    loadLatestTracks();
    loadGenres();
});

// Event Listeners
function initializeEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            navigateToSection(section);
        });
    });

    document.querySelectorAll('[data-section]').forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            const section = el.dataset.section;
            navigateToSection(section);
        });
    });

    // Player Controls
    playPauseBtn.addEventListener('click', togglePlayPause);
    prevBtn.addEventListener('click', playPrevious);
    nextBtn.addEventListener('click', playNext);
    shuffleBtn.addEventListener('click', toggleShuffle);
    repeatBtn.addEventListener('click', toggleRepeat);

    // Audio Events
    audioPlayer.addEventListener('timeupdate', updateProgress);
    audioPlayer.addEventListener('loadedmetadata', updateDuration);
    audioPlayer.addEventListener('ended', handleTrackEnd);

    // Progress Bar
    progressBar.addEventListener('click', seekToPosition);

    // Volume Controls
    volumeSlider.addEventListener('input', (e) => {
        state.volume = e.target.value / 100;
        audioPlayer.volume = state.volume;
        updateVolumeIcon();
    });

    volumeBtn.addEventListener('click', toggleMute);

    // Search
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    // Upload Modal
    uploadBtn.addEventListener('click', () => uploadModal.classList.add('active'));
    closeModal.addEventListener('click', () => uploadModal.classList.remove('active'));
    cancelUpload.addEventListener('click', () => uploadModal.classList.remove('active'));
    uploadModal.addEventListener('click', (e) => {
        if (e.target === uploadModal) uploadModal.classList.remove('active');
    });

    // Upload Form
    uploadForm.addEventListener('submit', handleUpload);

    // Filters
    genreFilter.addEventListener('change', loadAllTracks);
    sortFilter.addEventListener('change', loadAllTracks);

    // Hero Buttons
    document.getElementById('playFeaturedBtn')?.addEventListener('click', () => {
        loadFeaturedTracks().then(() => {
            if (state.queue.length > 0) {
                playTrack(0);
            }
        });
    });

    document.getElementById('browseBtn')?.addEventListener('click', () => {
        navigateToSection('tracks');
    });
}

// Navigation
function navigateToSection(section) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.section === section) {
            link.classList.add('active');
        }
    });

    // Show/hide sections
    const sections = {
        home: ['homeSection', 'featuredSection', 'latestSection'],
        tracks: ['tracksSection'],
        favorites: ['favoritesSection'],
        artists: ['artistsSection'],
        genres: ['genresSection']
    };

    // Hide all sections first
    document.querySelectorAll('.section, .hero').forEach(el => {
        el.style.display = 'none';
    });

    // Show appropriate sections
    if (section === 'home') {
        document.querySelector('.hero').style.display = 'flex';
        sections.home.forEach(id => {
            document.getElementById(id).style.display = 'block';
        });
        loadFeaturedTracks();
        loadLatestTracks();
    } else if (section === 'tracks') {
        document.getElementById('tracksSection').style.display = 'block';
        loadAllTracks();
    } else if (section === 'favorites') {
        document.getElementById('favoritesSection').style.display = 'block';
        loadFavorites();
    } else if (section === 'artists') {
        document.getElementById('artistsSection').style.display = 'block';
        loadArtists();
    } else if (section === 'genres') {
        document.getElementById('genresSection').style.display = 'block';
        loadGenres();
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// API Functions
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showToast('Error loading data', 'error');
        return null;
    }
}

async function loadFeaturedTracks() {
    const container = document.getElementById('featuredTracks');
    if (!container) return;

    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    const tracks = await fetchAPI('/featured?limit=8');
    if (tracks) {
        state.featuredTracks = tracks;
        container.innerHTML = tracks.map((track, index) => createTrackCard(track, index)).join('');
    } else {
        container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No tracks available</p>';
    }
}

async function loadLatestTracks() {
    const container = document.getElementById('latestTracks');
    if (!container) return;

    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    const tracks = await fetchAPI('/latest?limit=8');
    if (tracks) {
        state.latestTracks = tracks;
        container.innerHTML = tracks.map((track, index) => createTrackCard(track, index)).join('');
    } else {
        container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No tracks available</p>';
    }
}

async function loadAllTracks() {
    const container = document.getElementById('allTracks');
    if (!container) return;

    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    let endpoint = '/tracks?limit=100';
    
    if (genreFilter.value) {
        endpoint += `&genre=${encodeURIComponent(genreFilter.value)}`;
    }

    const tracks = await fetchAPI(endpoint);
    
    if (tracks) {
        // Sort tracks
        if (sortFilter.value === 'popular') {
            tracks.sort((a, b) => b.plays - a.plays);
        } else if (sortFilter.value === 'az') {
            tracks.sort((a, b) => a.title.localeCompare(b.title));
        } else {
            tracks.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        }

        state.allTracks = tracks;
        container.innerHTML = tracks.map((track, index) => createTrackListItem(track, index)).join('');
    } else {
        container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No tracks available</p>';
    }
}

async function loadArtists() {
    const container = document.getElementById('artistsGrid');
    if (!container) return;

    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    const artists = await fetchAPI('/artists');
    if (artists) {
        container.innerHTML = artists.map(artist => `
            <div class="artist-card">
                <img src="${artist.image_url || 'assets/images/logo.png'}" alt="${artist.name}" class="artist-image">
                <h3 class="artist-name">${artist.name}</h3>
                <p class="artist-bio">${artist.bio || 'Artist'}</p>
            </div>
        `).join('');
    } else {
        container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No artists available</p>';
    }
}

async function loadGenres() {
    const container = document.getElementById('genresGrid');
    const filterContainer = document.getElementById('genreFilter');
    
    const data = await fetchAPI('/genres');
    
    if (data && data.genres) {
        const genres = data.genres;
        
        // Update filter dropdown
        filterContainer.innerHTML = '<option value="">All Genres</option>' +
            genres.map(genre => `<option value="${genre}">${genre}</option>`).join('');
        
        // Update genres grid
        if (container) {
            const genreIcons = {
                'Amapiano': 'fa-music',
                'Afro House': 'fa-house-user',
                'Hip Hop': 'fa-microphone',
                'R&B': 'fa-heart',
                'Gqom': 'fa-drum',
                'Afrobeat': 'fa-guitar',
                'Other': 'fa-ellipsis-h'
            };

            container.innerHTML = genres.map(genre => `
                <div class="genre-card" onclick="filterByGenre('${genre}')">
                    <i class="fas ${genreIcons[genre] || 'fa-music'} genre-icon"></i>
                    <h3 class="genre-name">${genre}</h3>
                </div>
            `).join('');
        }
    }
}

async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    navigateToSection('tracks');
    
    const container = document.getElementById('allTracks');
    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    const tracks = await fetchAPI(`/search?q=${encodeURIComponent(query)}`);
    
    if (tracks && tracks.length > 0) {
        state.allTracks = tracks;
        container.innerHTML = tracks.map((track, index) => createTrackListItem(track, index)).join('');
    } else {
        container.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No tracks found</p>';
    }
}

async function loadFavorites() {
    const container = document.getElementById('favoritesList');
    const noFavorites = document.getElementById('noFavorites');
    
    if (!container) return;

    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    // Get all tracks and filter by liked IDs
    const allTracks = await fetchAPI('/tracks?limit=100');
    
    if (allTracks && state.likedTracks.length > 0) {
        const likedTracks = allTracks.filter(track => state.likedTracks.includes(track.id));
        
        if (likedTracks.length > 0) {
            container.innerHTML = likedTracks.map((track, index) => createTrackListItem(track, index)).join('');
            noFavorites.style.display = 'none';
        } else {
            container.innerHTML = '';
            noFavorites.style.display = 'block';
        }
    } else {
        container.innerHTML = '';
        noFavorites.style.display = 'block';
    }
}

// Track Card HTML
function createTrackCard(track, index) {
    const trackSlug = createTrackSlug(track);
    const trackUrl = `${window.location.origin}/track/${track.id}`;

    return `
        <div class="track-card" onclick="playTrackFromQueue(${index}, 'featured')">
            <div class="play-overlay">
                <i class="fas fa-play-circle"></i>
            </div>
            <img src="${track.cover_url || 'assets/images/logo.png'}" alt="${track.title}" class="track-cover" onerror="this.src='assets/images/logo.png'">
            <div class="track-info">
                <h3 class="track-title">${track.title}</h3>
                <p class="track-artist">${track.artist}</p>
                <div class="track-meta">
                    <span><i class="fas fa-play"></i> ${formatNumber(track.plays)}</span>
                    ${track.genre ? `<span><i class="fas fa-tag"></i> ${track.genre}</span>` : ''}
                </div>
                <div class="track-actions">
                    <button class="action-btn" onclick="event.stopPropagation(); toggleLike('${track.id}')" title="${state.likedTracks.includes(track.id) ? 'Unlike' : 'Like'}">
                        <i class="fas ${state.likedTracks.includes(track.id) ? 'fa-heart' : 'fa-heart'}" style="color: ${state.likedTracks.includes(track.id) ? '#ef4444' : ''}"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); downloadTrack('${track.file_url}', '${escapeHtml(track.title)}')" title="Download">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); shareTrack('${escapeHtml(track.title)}', '${escapeHtml(track.artist)}', '${trackUrl}')" title="Share">
                        <i class="fas fa-share-alt"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); copyLink('${trackUrl}')" title="Copy Link">
                        <i class="fas fa-link"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); openTrackDetail('${track.id}')" title="View Details">
                        <i class="fas fa-info-circle"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Track List Item HTML
function createTrackListItem(track, index) {
    const trackUrl = `${window.location.origin}/track/${track.id}`;
    
    return `
        <div class="track-item" onclick="playTrackFromQueue(${index}, 'all')">
            <img src="${track.cover_url || 'assets/images/logo.png'}" alt="${track.title}" class="track-item-image" onerror="this.src='assets/images/logo.png'">
            <div class="track-item-info">
                <h4 class="track-item-title">${track.title}</h4>
                <p class="track-item-artist">${track.artist}</p>
            </div>
            <div class="track-item-actions">
                <button class="track-item-btn" onclick="event.stopPropagation(); toggleLike('${track.id}')" title="${state.likedTracks.includes(track.id) ? 'Unlike' : 'Like'}">
                    <i class="fas ${state.likedTracks.includes(track.id) ? 'fa-heart' : 'fa-heart'}" style="color: ${state.likedTracks.includes(track.id) ? '#ef4444' : ''}"></i>
                </button>
                <button class="track-item-btn" onclick="event.stopPropagation(); downloadTrack('${track.file_url}', '${escapeHtml(track.title)}')" title="Download">
                    <i class="fas fa-download"></i>
                </button>
                <button class="track-item-btn" onclick="event.stopPropagation(); shareTrack('${escapeHtml(track.title)}', '${escapeHtml(track.artist)}', '${trackUrl}')" title="Share">
                    <i class="fas fa-share-alt"></i>
                </button>
                <button class="track-item-btn" onclick="event.stopPropagation(); copyLink('${trackUrl}')" title="Copy Link">
                    <i class="fas fa-link"></i>
                </button>
                <button class="track-item-btn" onclick="event.stopPropagation(); playTrackFromQueue(${index}, 'all')">
                    <i class="fas fa-play"></i>
                </button>
            </div>
        </div>
    `;
}

// Player Functions
function playTrackFromQueue(index, queueType) {
    const queueMap = {
        'featured': state.featuredTracks,
        'latest': state.latestTracks,
        'all': state.allTracks
    };

    const queue = queueMap[queueType];
    if (!queue || !queue[index]) return;

    state.queue = queue;
    state.queueIndex = index;
    playTrack(index);
}

function playTrack(index) {
    const track = state.queue[index];
    if (!track) return;

    state.currentTrack = track;
    state.queueIndex = index;

    // Update player UI
    playerTitle.textContent = track.title;
    playerArtist.textContent = track.artist;
    playerCover.src = track.cover_url || 'assets/images/logo.png';

    // Load and play audio
    // For demo purposes, we'll use a placeholder audio
    // In production, this would be: audioPlayer.src = `${API_BASE_URL}${track.file_url}`;
    audioPlayer.src = track.file_url || '';
    
    audioPlayer.play().then(() => {
        state.isPlaying = true;
        updatePlayPauseButton();
        // Add to recently played
        addToRecentlyPlayed(track);
    }).catch(error => {
        console.log('Playback failed:', error);
        showToast('Unable to play track (demo mode)', 'error');
    });

    // Highlight current track
    document.querySelectorAll('.track-card, .track-item').forEach((el, i) => {
        el.classList.remove('now-playing');
        if (i === index) {
            el.classList.add('now-playing');
        }
    });
}

function togglePlayPause() {
    if (!state.currentTrack) {
        if (state.queue.length > 0) {
            playTrack(0);
        }
        return;
    }

    if (state.isPlaying) {
        audioPlayer.pause();
    } else {
        audioPlayer.play();
    }
    state.isPlaying = !state.isPlaying;
    updatePlayPauseButton();
}

function updatePlayPauseButton() {
    const icon = playPauseBtn.querySelector('i');
    if (state.isPlaying) {
        icon.classList.remove('fa-play');
        icon.classList.add('fa-pause');
    } else {
        icon.classList.remove('fa-pause');
        icon.classList.add('fa-play');
    }
}

function playPrevious() {
    if (state.queueIndex > 0) {
        playTrack(state.queueIndex - 1);
    } else if (state.repeatMode === 'all') {
        playTrack(state.queue.length - 1);
    }
}

function playNext() {
    if (state.queueIndex < state.queue.length - 1) {
        playTrack(state.queueIndex + 1);
    } else if (state.repeatMode === 'all') {
        playTrack(0);
    }
}

function handleTrackEnd() {
    if (state.repeatMode === 'one') {
        audioPlayer.currentTime = 0;
        audioPlayer.play();
    } else {
        playNext();
    }
}

function toggleShuffle() {
    state.isShuffle = !state.isShuffle;
    shuffleBtn.style.color = state.isShuffle ? 'var(--primary-color)' : '';
    
    if (state.isShuffle && state.queue.length > 1) {
        const current = state.queue[state.queueIndex];
        for (let i = state.queue.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [state.queue[i], state.queue[j]] = [state.queue[j], state.queue[i]];
        }
        state.queueIndex = state.queue.indexOf(current);
    }
}

function toggleRepeat() {
    const modes = ['none', 'all', 'one'];
    const currentIndex = modes.indexOf(state.repeatMode);
    state.repeatMode = modes[(currentIndex + 1) % modes.length];
    
    const icon = repeatBtn.querySelector('i');
    if (state.repeatMode === 'one') {
        icon.classList.add('fa-redo');
        repeatBtn.style.color = 'var(--primary-color)';
    } else if (state.repeatMode === 'all') {
        repeatBtn.style.color = 'var(--primary-color)';
    } else {
        repeatBtn.style.color = '';
    }
}

function updateProgress() {
    const percent = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    progress.style.width = `${percent}%`;
    currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
}

function updateDuration() {
    durationEl.textContent = formatTime(audioPlayer.duration);
}

function seekToPosition(e) {
    const rect = progressBar.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    audioPlayer.currentTime = percent * audioPlayer.duration;
}

function toggleMute() {
    if (audioPlayer.muted) {
        audioPlayer.muted = false;
        state.volume = volumeSlider.value / 100;
        audioPlayer.volume = state.volume;
    } else {
        audioPlayer.muted = true;
    }
    updateVolumeIcon();
}

function updateVolumeIcon() {
    const icon = volumeBtn.querySelector('i');
    if (audioPlayer.muted || state.volume === 0) {
        icon.className = 'fas fa-volume-mute';
    } else if (state.volume < 0.5) {
        icon.className = 'fas fa-volume-down';
    } else {
        icon.className = 'fas fa-volume-up';
    }
}

// Upload Functions
async function handleUpload(e) {
    e.preventDefault();

    const formData = new FormData(uploadForm);

    try {
        const response = await fetch(`${API_BASE_URL}/tracks`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            showToast('Track uploaded successfully!', 'success');
            uploadModal.classList.remove('active');
            uploadForm.reset();
            loadAllTracks();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Upload failed', 'error');
        }
    } catch (error) {
        showToast('Upload failed. Make sure the server is running.', 'error');
    }
}

// New Track Actions Functions
function downloadTrack(fileUrl, title) {
    if (!fileUrl) {
        showToast('Download not available for this track', 'warning');
        return;
    }

    // Create a clean filename (remove special characters)
    const cleanTitle = (title || 'track')
        .replace(/[^a-zA-Z0-9\s-]/g, '')  // Remove special chars
        .replace(/\s+/g, '-')              // Replace spaces with dashes
        .substring(0, 50);                 // Limit length
    
    // Create download link
    const link = document.createElement('a');
    link.href = fileUrl;
    link.download = `${cleanTitle}.mp3`;
    link.rel = 'noopener noreferrer';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast('Download started!', 'success');
}

function shareTrack(title, artist, trackUrl) {
    const shareData = {
        title: title,
        text: `Check out "${title}" by ${artist} on DGT-SOUNDS!`,
        url: trackUrl
    };
    
    // Check if Web Share API is supported
    if (navigator.share) {
        navigator.share(shareData)
            .then(() => showToast('Shared successfully!', 'success'))
            .catch((error) => console.log('Share failed:', error));
    } else {
        // Fallback: show share options
        const shareOptions = `
            Share "${title}" by ${artist}:
            %0A%0A🎵 ${shareData.text}
            %0A🔗 ${trackUrl}
        `;
        
        const options = [
            { name: 'WhatsApp', url: `https://wa.me/?text=${shareOptions}`, icon: 'fab fa-whatsapp', color: '#25D366' },
            { name: 'Facebook', url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(trackUrl)}`, icon: 'fab fa-facebook', color: '#1877F2' },
            { name: 'Twitter', url: `https://twitter.com/intent/tweet?text=${shareData.text}&url=${encodeURIComponent(trackUrl)}`, icon: 'fab fa-twitter', color: '#1DA1F2' },
            { name: 'Copy Link', action: 'copy', icon: 'fas fa-link', color: 'var(--primary-color)' }
        ];
        
        const modal = document.createElement('div');
        modal.className = 'share-modal';
        modal.innerHTML = `
            <div class="share-modal-content">
                <div class="share-modal-header">
                    <h3>Share "${title}"</h3>
                    <button class="share-modal-close" onclick="this.closest('.share-modal').remove()">&times;</button>
                </div>
                <div class="share-modal-body">
                    ${options.map(opt => `
                        <a href="${opt.url}" target="_blank" class="share-option" style="border-left: 4px solid ${opt.color};" 
                           onclick="${opt.action === 'copy' ? `event.preventDefault(); copyLink('${trackUrl}'); this.closest('.share-modal').remove();` : ''}">
                            <i class="${opt.icon}" style="color: ${opt.color};"></i>
                            <span>${opt.name}</span>
                        </a>
                    `).join('')}
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        setTimeout(() => modal.classList.add('active'), 10);
    }
}

function copyLink(url) {
    navigator.clipboard.writeText(url).then(() => {
        showToast('Link copied to clipboard!', 'success');
    }).catch(() => {
        // Fallback for older browsers
        const input = document.createElement('input');
        input.value = url;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        document.body.removeChild(input);
        showToast('Link copied to clipboard!', 'success');
    });
}

function toggleLike(trackId) {
    const index = state.likedTracks.indexOf(trackId);
    if (index > -1) {
        // Unlike
        state.likedTracks.splice(index, 1);
        showToast('Removed from favorites', 'success');
    } else {
        // Like
        state.likedTracks.push(trackId);
        showToast('Added to favorites! ❤️', 'success');
    }
    // Save to localStorage
    localStorage.setItem('likedTracks', JSON.stringify(state.likedTracks));
    // Refresh UI
    loadFeaturedTracks();
    loadLatestTracks();
    loadAllTracks();
}

function addToRecentlyPlayed(track) {
    // Remove if already exists
    state.recentlyPlayed = state.recentlyPlayed.filter(t => t.id !== track.id);
    // Add to beginning
    state.recentlyPlayed.unshift({
        id: track.id,
        title: track.title,
        artist: track.artist,
        cover_url: track.cover_url,
        playedAt: new Date().toISOString()
    });
    // Keep only last 20
    if (state.recentlyPlayed.length > 20) {
        state.recentlyPlayed = state.recentlyPlayed.slice(0, 20);
    }
    // Save to localStorage
    localStorage.setItem('recentlyPlayed', JSON.stringify(state.recentlyPlayed));
}

function openTrackDetail(trackId) {
    // Fetch track details and show in modal
    fetch(`${API_BASE_URL}/tracks/${trackId}`)
        .then(res => res.json())
        .then(track => {
            if (track) {
                const trackUrl = `${window.location.origin}/track/${trackId}`;
                const modal = document.createElement('div');
                modal.className = 'track-detail-modal';
                modal.innerHTML = `
                    <div class="track-detail-content">
                        <button class="track-detail-close" onclick="this.closest('.track-detail-modal').remove()">&times;</button>
                        <div class="track-detail-header">
                            <img src="${track.cover_url || 'assets/images/logo.png'}" alt="${track.title}" class="track-detail-cover" onerror="this.src='assets/images/logo.png'">
                            <div class="track-detail-info">
                                <h2>${track.title}</h2>
                                <p class="track-detail-artist">${track.artist}</p>
                                ${track.album ? `<p class="track-detail-album">Album: ${track.album}</p>` : ''}
                                ${track.genre ? `<span class="track-detail-genre">${track.genre}</span>` : ''}
                                <div class="track-detail-stats">
                                    <span><i class="fas fa-play"></i> ${formatNumber(track.plays)} plays</span>
                                </div>
                            </div>
                        </div>
                        <div class="track-detail-actions">
                            <button class="btn btn-primary" onclick="playTrackFromQueue(0, 'detail'); this.closest('.track-detail-modal').remove();">
                                <i class="fas fa-play"></i> Play
                            </button>
                            <button class="btn btn-secondary" onclick="downloadTrack('${track.file_url}', '${escapeHtml(track.title)}')">
                                <i class="fas fa-download"></i> Download
                            </button>
                            <button class="btn btn-secondary" onclick="shareTrack('${escapeHtml(track.title)}', '${escapeHtml(track.artist)}', '${trackUrl}')">
                                <i class="fas fa-share-alt"></i> Share
                            </button>
                            <button class="btn btn-secondary" onclick="copyLink('${trackUrl}')">
                                <i class="fas fa-link"></i> Copy Link
                            </button>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
                setTimeout(() => modal.classList.add('active'), 10);
                
                // Add to queue for playing
                state.detailQueue = [track];
            }
        })
        .catch(err => showToast('Error loading track details', 'error'));
}

function createTrackSlug(track) {
    // Create URL-friendly slug from track title and artist
    const title = track.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const artist = track.artist.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    return `${artist}-${title}`;
}

function escapeHtml(text) {
    // Escape HTML to prevent XSS attacks
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Utility Functions
function filterByGenre(genre) {
    genreFilter.value = genre;
    navigateToSection('tracks');
    loadAllTracks();
}

function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;

    switch(e.code) {
        case 'Space':
            e.preventDefault();
            togglePlayPause();
            break;
        case 'ArrowLeft':
            playPrevious();
            break;
        case 'ArrowRight':
            playNext();
            break;
        case 'ArrowUp':
            e.preventDefault();
            state.volume = Math.min(1, state.volume + 0.1);
            volumeSlider.value = state.volume * 100;
            audioPlayer.volume = state.volume;
            updateVolumeIcon();
            break;
        case 'ArrowDown':
            e.preventDefault();
            state.volume = Math.max(0, state.volume - 0.1);
            volumeSlider.value = state.volume * 100;
            audioPlayer.volume = state.volume;
            updateVolumeIcon();
            break;
    }
});
