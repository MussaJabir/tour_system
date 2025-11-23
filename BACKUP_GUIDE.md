# 💾 Database Backup Guide

## 🎯 Quick Start

### Manual Backup (Anytime):
```bash
./backup.sh
```

### Manual Backup with Custom Name:
```bash
./backup.sh "before_payment_feature"
```

### Restore from Backup:
```bash
./restore.sh backups/manual_backup_20251116_010000.sql.gz
```

### Enable Automated Daily Backups:
```bash
docker-compose -f docker-compose.yml -f docker-compose.backup.yml up -d
```

---

## 📁 What You Have Now

### Files Created:
1. **`backup.sh`** - Manual backup anytime
2. **`restore.sh`** - Restore from backup
3. **`docker-compose.backup.yml`** - Automated daily backups
4. **`backups/`** - Folder where backups are stored

---

## 🔧 How to Use

### 1. Create Manual Backup
```bash
./backup.sh
```
**Output:**
```
🔄 Starting database backup...
📦 Creating backup: manual_backup_20251116_010000.sql.gz
✅ Backup completed successfully!
📁 File: ./backups/manual_backup_20251116_010000.sql.gz
💾 Size: 2.3M
```

### 2. List All Backups
```bash
ls -lh backups/
```

### 3. Restore from Backup
```bash
./restore.sh backups/manual_backup_20251116_010000.sql.gz
```
**Prompts:**
```
⚠️  WARNING: This will REPLACE your current database!
Are you sure you want to continue? (yes/no):
```

---

## 🤖 Automated Backups

### Start Automated Backup Service:
```bash
docker-compose -f docker-compose.yml -f docker-compose.backup.yml up -d backup
```

### What It Does:
- ✅ Runs backup every day at **2:00 AM**
- ✅ Saves as: `auto_backup_YYYYMMDD_HHMMSS.sql.gz`
- ✅ Keeps last **30 days** (auto-cleanup)
- ✅ Compressed to save space

### Check Backup Service Status:
```bash
docker-compose logs backup
```

### Stop Automated Backups:
```bash
docker-compose stop backup
```

---

## 📊 Backup Naming Convention

| Type | Format | Example |
|------|--------|---------|
| **Manual** | `manual_backup_YYYYMMDD_HHMMSS.sql.gz` | `manual_backup_20251116_010000.sql.gz` |
| **Custom** | `your_name.sql.gz` | `before_payment_feature.sql.gz` |
| **Automated** | `auto_backup_YYYYMMDD_HHMMSS.sql.gz` | `auto_backup_20251116_020000.sql.gz` |
| **Safety** | `pre_restore_YYYYMMDD_HHMMSS.sql.gz` | `pre_restore_20251116_030000.sql.gz` |

---

## 🚨 Important: When to Backup

### Always backup before:
- ✅ Major code deployments
- ✅ Database migrations
- ✅ Testing risky features
- ✅ Making bulk data changes

### Quick Commands:
```bash
# Before deployment
./backup.sh "before_v2_deployment"

# Before migration
./backup.sh "before_migration_$(date +%Y%m%d)"

# Before testing
./backup.sh "before_payment_test"
```

---

## 🔄 Restore Safety Features

### Automatic Safety Backup:
When you run `./restore.sh`, it **automatically creates a safety backup** of your current database first!

**Example:**
```bash
./restore.sh backups/old_backup.sql.gz

# Output:
📦 Creating safety backup before restore...
✅ Safety backup created: ./backups/pre_restore_20251116_030000.sql.gz
🔄 Restoring database...
✅ Database restored successfully!
```

**If restore fails, you can rollback:**
```bash
./restore.sh backups/pre_restore_20251116_030000.sql.gz
```

---

## 📈 Best Practices

### Daily Workflow:
```bash
# Morning: Start automated backups (once)
docker-compose -f docker-compose.yml -f docker-compose.backup.yml up -d

# Before major change: Manual backup
./backup.sh "before_big_feature"

# If something goes wrong: Restore
./restore.sh backups/before_big_feature.sql.gz
```

### Storage Management:
- Automated backups keep **30 days** (auto-cleanup)
- Manual backups **never auto-delete** (you control them)
- Check backup size: `du -sh backups/`

---

## 🎯 Real-World Scenarios

### Scenario 1: Accidental Data Deletion
```bash
# Oh no! Deleted important bookings
./restore.sh backups/auto_backup_20251115_020000.sql.gz
docker-compose restart django
# Data restored! ✅
```

### Scenario 2: Failed Migration
```bash
# Before migration
./backup.sh "before_packages_migration"
python manage.py migrate

# Migration broke something?
./restore.sh backups/before_packages_migration.sql.gz
# Back to working state! ✅
```

### Scenario 3: Testing Dangerous Code
```bash
# Before testing payment deletion
./backup.sh "before_payment_delete_test"

# Test the code... breaks everything

# Restore
./restore.sh backups/before_payment_delete_test.sql.gz
# Clean slate! ✅
```

---

## 💡 Pro Tips

1. **Name your backups descriptively**
   ```bash
   ./backup.sh "before_inquiry_phase2"  # Good ✅
   ./backup.sh "backup1"                 # Bad ❌
   ```

2. **Check backup success**
   ```bash
   ls -lh backups/*.sql.gz | tail -1
   # Should show file > 0 bytes
   ```

3. **Backup before Friday deployments**
   ```bash
   # Friday afternoon
   ./backup.sh "friday_safe_backup_$(date +%Y%m%d)"
   # Relax over weekend knowing you can restore ✅
   ```

4. **Keep important milestone backups**
   ```bash
   # After completing major feature
   ./backup.sh "phase2_complete_working"
   # Never auto-deleted, always available
   ```

---

## ✅ Summary

**You now have:**
- ✅ Manual backup anytime: `./backup.sh`
- ✅ Restore with safety: `./restore.sh <file>`
- ✅ Automated daily backups (optional)
- ✅ 30-day retention
- ✅ Compressed storage
- ✅ Safety backup before restore

**Your data is now PROTECTED!** 🛡️

