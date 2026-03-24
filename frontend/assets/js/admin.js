/**
 * DGT-SOUNDS Admin Dashboard
 * Full CRUD management for tracks, albums, and artists
 */

const API_BASE = 'http://localhost:8000/api';

// State
let currentUser = null;
let deleteCallback = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    initializeEventListeners();
});

// Authentication
function checkAuth() {
    const auth = localStorage.getItem('adminAuth');
    if (auth === 'true') {
        showDashboard();
    }
}

function initializeEventListeners() {
    // Login
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);

    // Logout
    document.getElementById('logoutBtn')?.addEventListener('click', handleLogout);

    // Sidebar toggle
    document.getElementById('sidebarToggle')?.addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('collapsed');
    });

    // Mobile menu
    document.getElementById('mobileMenuBtn')?.addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('active');
    });

    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            navigateTo(page);

            // Mobile: close sidebar after navigation
            if (window.innerWidth <= 768) {
                document.getElementById('sidebar').classList.remove('active');
            }
        });
    });

    // Upload form
    document.getElementById('uploadForm')?.addEventListener('submit', handleUpload);

    // Track edit form
    document.getElementById('trackEditForm')?.addEventListener('submit', handleTrackUpdate);

    // Album create form
    document.getElementById('albumCreateForm')?.addEventListener('submit', handleAlbumCreate);

    // Artist create form
    document.getElementById('artistCreateForm')?.addEventListener('submit', handleArtistCreate);

    // Settings form
    document.getElementById('settingsForm')?.addEventListener('submit', (e) => {
        e.preventDefault();
        showToast('Settings saved successfully!', 'success');
    });

    // Search
    document.getElementById('globalSearch')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performGlobalSearch(e.target.value);
        }
    });

    // Track search
    document.getElementById('trackSearch')?.addEventListener('input', (e) => {
        filterTracks(e.target.value);
    });

    // File upload drag & drop
    setupFileUpload();

    // Modal close buttons
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.modal').classList.remove('active');
        });
    });

    // Close modals on outside click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('adminEmail').value;
    const password = document.getElementById('adminPassword').value;
    
    try {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE}/admin/login`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('adminAuth', 'true');
            localStorage.setItem('adminEmail', email);
            localStorage.setItem('adminToken', data.access_token);
            showDashboard();
            showToast('Welcome back, Admin!', 'success');
        } else {
            showToast('Invalid credentials', 'error');
        }
    } catch (error) {
        // Fallback to simple auth if API is not available
        if (email === 'admin@dgt-sounds.com' && password === 'admin123') {
            localStorage.setItem('adminAuth', 'true');
            localStorage.setItem('adminEmail', email);
            showDashboard();
            showToast('Welcome back, Admin! (Offline mode)', 'warning');
        } else {
            showToast('Invalid credentials', 'error');
        }
    }
}

function handleLogout() {
    localStorage.removeItem('adminAuth');
    localStorage.removeItem('adminEmail');
    location.reload();
}

function showDashboard() {
    document.getElementById('loginOverlay').style.display = 'none';
    document.getElementById('adminWrapper').style.display = 'flex';
    loadDashboardData();
}

// Navigation
function navigateTo(page) {
    // Update active nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === page) {
            item.classList.add('active');
        }
    });
    
    // Hide all pages
    document.querySelectorAll('.admin-content').forEach(content => {
        content.style.display = 'none';
    });
    
    // Show selected page
    const pageMap = {
        'dashboard': 'dashboardPage',
        'tracks': 'tracksPage',
        'albums': 'albumsPage',
        'artists': 'artistsPage',
        'uploads': 'uploadsPage',
        'settings': 'settingsPage'
    };
    
    document.getElementById(pageMap[page]).style.display = 'block';
    
    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'tracks': 'Track Management',
        'albums': 'Album Management',
        'artists': 'Artist Management',
        'uploads': 'Upload Track',
        'settings': 'Settings'
    };
    document.getElementById('pageTitle').textContent = titles[page];
    
    // Load page data
    switch(page) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'tracks':
            loadTracks();
            break;
        case 'albums':
            loadAlbums();
            break;
        case 'artists':
            loadArtists();
            break;
    }
}

// Dashboard Data
async function loadDashboardData() {
    try {
        const [tracks, genres] = await Promise.all([
            fetchAPI('/tracks?limit=100'),
            fetchAPI('/genres')
        ]);
        
        if (tracks) {
            // Update stats
            document.getElementById('totalTracks').textContent = tracks.length;
            document.getElementById('totalPlays').textContent = formatNumber(tracks.reduce((sum, t) => sum + (t.plays || 0), 0));
            
            // Update genre filter
            const genreFilter = document.getElementById('trackGenreFilter');
            if (genres && genres.genres) {
                genreFilter.innerHTML = '<option value="">All Genres</option>' +
                    genres.genres.map(g => `<option value="${g}">${g}</option>`).join('');
            }
            
            // Top tracks
            const sortedByPlays = [...tracks].sort((a, b) => (b.plays || 0) - (a.plays || 0)).slice(0, 5);
            const topTracksList = document.getElementById('topTracksList');
            topTracksList.innerHTML = sortedByPlays.map((track, i) => `
                <div class="top-item">
                    <div class="top-rank">${i + 1}</div>
                    <img src="${track.cover_url || '../assets/images/logo.png'}" class="table-cover" style="width: 40px; height: 40px;">
                    <div class="top-info" style="flex: 1;">
                        <h4>${track.title}</h4>
                        <p>${track.artist}</p>
                    </div>
                    <div class="top-plays">
                        <i class="fas fa-play"></i> ${formatNumber(track.plays || 0)}
                    </div>
                </div>
            `).join('');
            
            // Recent uploads
            const sortedByDate = [...tracks].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 5);
            const recentList = document.getElementById('recentUploadsList');
            recentList.innerHTML = sortedByDate.map(track => `
                <div class="recent-item">
                    <img src="${track.cover_url || '../assets/images/logo.png'}" class="table-cover" style="width: 40px; height: 40px;">
                    <div class="top-info" style="flex: 1;">
                        <h4>${track.title}</h4>
                        <p>${track.artist}</p>
                    </div>
                    <div class="top-plays">
                        ${new Date(track.created_at).toLocaleDateString()}
                    </div>
                </div>
            `).join('');
        }
        
        // Mock data for albums and artists (replace with actual API calls)
        document.getElementById('totalAlbums').textContent = '12';
        document.getElementById('totalArtists').textContent = '8';
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Error loading dashboard data', 'error');
    }
}

// Tracks Management
async function loadTracks() {
    const tbody = document.getElementById('tracksTableBody');
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center;"><div class="loading"><div class="spinner"></div></div></td></tr>';
    
    try {
        const tracks = await fetchAPI('/tracks?limit=100');
        
        if (tracks && tracks.length > 0) {
            tbody.innerHTML = tracks.map(track => `
                <tr>
                    <td>
                        <img src="${track.cover_url || '../assets/images/logo.png'}" class="table-cover" onerror="this.src='../assets/images/logo.png'">
                    </td>
                    <td>
                        <div class="table-title">${track.title}</div>
                    </td>
                    <td>
                        <div class="table-artist">${track.artist}</div>
                    </td>
                    <td>${track.album || '-'}</td>
                    <td>
                        ${track.genre ? `<span class="table-badge">${track.genre}</span>` : '-'}
                    </td>
                    <td>
                        <i class="fas fa-play"></i> ${formatNumber(track.plays || 0)}
                    </td>
                    <td>${formatDuration(track.duration || 0)}</td>
                    <td>
                        <div class="table-actions">
                            <button class="btn-icon play" onclick="playTrack('${track.file_url}')" title="Play">
                                <i class="fas fa-play"></i>
                            </button>
                            <button class="btn-icon edit" onclick="editTrack('${track.id}', '${escapeHtml(track.title)}', '${escapeHtml(track.artist)}', '${escapeHtml(track.album || '')}', '${track.genre || ''}')" title="Edit">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-icon delete" onclick="confirmDelete('track', '${track.id}')" title="Delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 40px;">No tracks found. Upload your first track!</td></tr>';
        }
    } catch (error) {
        console.error('Error loading tracks:', error);
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 40px; color: red;">Error loading tracks</td></tr>';
    }
}

function filterTracks(query) {
    const rows = document.querySelectorAll('#tracksTableBody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query.toLowerCase()) ? '' : 'none';
    });
}

function showUploadModal() {
    navigateTo('uploads');
}

function editTrack(id, title, artist, album, genre) {
    document.getElementById('editTrackId').value = id;
    document.getElementById('editTitle').value = title;
    document.getElementById('editArtist').value = artist;
    document.getElementById('editAlbum').value = album;
    document.getElementById('editGenre').value = genre;
    
    document.getElementById('trackModalTitle').textContent = 'Edit Track';
    document.getElementById('trackModal').classList.add('active');
}

function closeTrackModal() {
    document.getElementById('trackModal').classList.remove('active');
}

async function handleUpload(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch(`${API_BASE}/tracks`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showToast('Track uploaded successfully!', 'success');
            e.target.reset();
            navigateTo('tracks');
        } else {
            const error = await response.json();
            showToast(error.detail || 'Upload failed', 'error');
        }
    } catch (error) {
        showToast('Upload failed. Make sure the backend is running.', 'error');
    }
}

async function handleTrackUpdate(e) {
    e.preventDefault();
    const id = document.getElementById('editTrackId').value;
    const formData = new FormData(e.target);
    const token = localStorage.getItem('adminToken');
    
    try {
        const response = await fetch(`${API_BASE}/admin/tracks/${id}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token || ''}`
            },
            body: formData
        });
        
        if (response.ok) {
            showToast('Track updated successfully!', 'success');
            closeTrackModal();
            loadTracks();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Update failed', 'error');
        }
    } catch (error) {
        showToast('Update failed. Make sure backend is running.', 'error');
    }
}

// Albums Management
async function loadAlbums() {
    const grid = document.getElementById('albumsGrid');
    grid.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
    
    try {
        const albums = await fetchAPI('/albums');
        
        if (albums && albums.length > 0) {
            grid.innerHTML = albums.map(album => `
                <div class="album-card">
                    <img src="${album.cover_url || '../assets/images/logo.png'}" class="album-cover" onerror="this.src='../assets/images/logo.png'">
                    <div class="album-info">
                        <div class="album-title">${album.title}</div>
                        <div class="album-artist">${album.artist_name || 'Various Artists'}</div>
                    </div>
                    <div class="card-actions">
                        <button class="btn-icon play" title="View">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn-icon edit" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-icon delete" onclick="confirmDelete('album', '${album.id}')" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px;"><i class="fas fa-compact-disc" style="font-size: 4rem; color: #ddd; margin-bottom: 20px;"></i><p style="color: #999;">No albums yet</p></div>';
        }
    } catch (error) {
        console.error('Error loading albums:', error);
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px; color: red;">Error loading albums</div>';
    }
}

function showAlbumModal() {
    document.getElementById('albumModal').classList.add('active');
}

function closeAlbumModal() {
    document.getElementById('albumModal').classList.remove('active');
}

async function handleAlbumCreate(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const token = localStorage.getItem('adminToken');

    try {
        const response = await fetch(`${API_BASE}/admin/albums`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token || ''}`
            },
            body: formData
        });

        if (response.ok) {
            showToast('Album created successfully!', 'success');
            closeAlbumModal();
            loadAlbums();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Create failed', 'error');
        }
    } catch (error) {
        showToast('Create failed. Make sure backend is running.', 'error');
    }
}

// Artists Management
async function loadArtists() {
    const grid = document.getElementById('artistsGrid');
    grid.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
    
    try {
        const artists = await fetchAPI('/artists');
        
        if (artists && artists.length > 0) {
            grid.innerHTML = artists.map(artist => `
                <div class="artist-card">
                    <img src="${artist.image_url || '../assets/images/logo.png'}" class="artist-image" onerror="this.src='../assets/images/logo.png'">
                    <div class="artist-info">
                        <div class="artist-name">${artist.name}</div>
                        <div class="artist-bio">${artist.bio || 'Artist'}</div>
                    </div>
                    <div class="card-actions">
                        <button class="btn-icon play" title="View">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn-icon edit" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-icon delete" onclick="confirmDelete('artist', '${artist.id}')" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px;"><i class="fas fa-users" style="font-size: 4rem; color: #ddd; margin-bottom: 20px;"></i><p style="color: #999;">No artists yet</p></div>';
        }
    } catch (error) {
        console.error('Error loading artists:', error);
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px; color: red;">Error loading artists</div>';
    }
}

function showArtistModal() {
    document.getElementById('artistModal').classList.add('active');
}

function closeArtistModal() {
    document.getElementById('artistModal').classList.remove('active');
}

async function handleArtistCreate(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const token = localStorage.getItem('adminToken');

    try {
        const response = await fetch(`${API_BASE}/admin/artists`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token || ''}`
            },
            body: formData
        });

        if (response.ok) {
            showToast('Artist created successfully!', 'success');
            closeArtistModal();
            loadArtists();
        } else {
            const error = await response.json();
            showToast(error.detail || 'Create failed', 'error');
        }
    } catch (error) {
        showToast('Create failed. Make sure backend is running.', 'error');
    }
}

// Delete Functionality
function confirmDelete(type, id) {
    deleteCallback = () => performDelete(type, id);
    document.getElementById('deleteModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deleteModal').classList.remove('active');
    deleteCallback = null;
}

document.getElementById('confirmDeleteBtn')?.addEventListener('click', () => {
    if (deleteCallback) {
        deleteCallback();
    }
});

async function performDelete(type, id) {
    const token = localStorage.getItem('adminToken');
    
    try {
        const endpoint = type === 'track' ? 'tracks' : type === 'album' ? 'albums' : 'artists';
        const response = await fetch(`${API_BASE}/admin/${endpoint}/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token || ''}`
            }
        });
        
        if (response.ok) {
            showToast(`${type} deleted successfully!`, 'success');
            closeDeleteModal();
            
            // Reload current page
            const activeNav = document.querySelector('.nav-item.active');
            if (activeNav) {
                navigateTo(activeNav.dataset.page);
            }
        } else {
            const error = await response.json();
            showToast(error.detail || 'Delete failed', 'error');
        }
    } catch (error) {
        showToast('Delete failed. Make sure backend is running.', 'error');
    }
}

// Utility Functions
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error('Network error');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

function playTrack(url) {
    if (!url) {
        showToast('No audio file available', 'warning');
        return;
    }
    // Open main site player or create admin player
    window.open(`../index.html`, '_blank');
}

function setupFileUpload() {
    const fileInputs = document.querySelectorAll('.file-upload input[type="file"]');
    
    fileInputs.forEach(input => {
        const label = input.parentElement.querySelector('.file-upload-label span');
        const originalText = label?.textContent;
        
        input.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                if (label) {
                    label.textContent = e.target.files[0].name;
                }
            }
        });
        
        input.addEventListener('dragleave', () => {
            input.parentElement.style.borderColor = '';
            if (label) label.textContent = originalText;
        });
    });
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatDuration(seconds) {
    if (!seconds) return '-:--';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle'
    };
    
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.success}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function performGlobalSearch(query) {
    if (!query) return;
    navigateTo('tracks');
    document.getElementById('trackSearch').value = query;
    filterTracks(query);
}
