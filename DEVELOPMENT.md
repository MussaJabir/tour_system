# Development vs Production Mode

## 🎯 What I Created

I've set up **two modes** for running your Docker containers:

### 1. **Development Mode** (Auto-reload enabled) 🔄
- Uses Django's `runserver` instead of Gunicorn
- **Automatically reloads** when you change Python files
- No need to restart Docker after code changes
- Better error messages and debugging

### 2. **Production Mode** (Standard setup) 🏭
- Uses Gunicorn (production server)
- Optimized for performance
- Requires manual restart after code changes

---

## 🚀 How to Use

### For Development (with auto-reload):
```bash
./dev.sh
```
Or manually:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### For Production:
```bash
./prod.sh
```
Or manually:
```bash
docker-compose up -d
```

---

## 📁 What Changed

### New Files Created:
1. **`docker-compose.dev.yml`** - Development overrides
2. **`dev.sh`** - Quick start script for development
3. **`prod.sh`** - Quick start script for production

### Key Differences:

| Feature | Development Mode | Production Mode |
|---------|-----------------|----------------|
| Server | Django runserver | Gunicorn |
| Auto-reload | ✅ Yes | ❌ No |
| Performance | Slower | Faster |
| Debugging | Better | Basic |
| Restart needed | ❌ No | ✅ Yes |

---

## 💡 How Auto-Reload Works

**Development Mode:**
1. You edit a Python file (e.g., `packages/views.py`)
2. Django's runserver detects the change
3. Server automatically reloads
4. Your changes are live immediately! ✨

**No more running:**
```bash
docker-compose restart django  # Not needed in dev mode!
```

---

## 🔍 When to Use Each Mode

### Use Development Mode when:
- ✅ Actively coding and testing
- ✅ Making frequent changes
- ✅ Need instant feedback
- ✅ Debugging issues

### Use Production Mode when:
- ✅ Deploying to server
- ✅ Performance testing
- ✅ Final testing before release
- ✅ Not making code changes

---

## 🛠️ Troubleshooting

### Development mode not reloading?
```bash
# Stop everything
docker-compose down

# Start fresh in dev mode
./dev.sh
```

### Want to see logs?
```bash
# In development (foreground - you'll see live logs)
./dev.sh

# In production (background)
./prod.sh
docker-compose logs -f django  # View logs
```

### Switch between modes:
```bash
# Stop current mode
docker-compose down

# Start new mode
./dev.sh   # or ./prod.sh
```

---

## 📊 Current Status

✅ Auto-reload is now configured!
✅ Development script ready
✅ Production script ready
✅ Easy switching between modes

**Recommendation:** Use `./dev.sh` during development to save time! 🚀

