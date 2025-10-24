# 🎉 New Features Testing Guide

## ✨ What's New?

You just added **2 powerful features**:

1. **📈 Rank Change Notifications** - Track LP gains/losses and promotions/demotions
2. **⚔️ Clash Tournament Tracker** - View upcoming Clash schedules

---

## 🧪 How to Test

### **Feature 1: Rank Change Notifications**

This feature automatically tracks LP changes for stalked players!

#### What It Does:
- Shows LP gains/losses after each match (e.g., "+17 LP 📈")
- Alerts when someone gets promoted (e.g., "🎉 PROMOTION! Silver III!")
- Alerts when someone gets demoted (e.g., "😢 Demoted to Silver IV")

#### How to Test:

1. **Start your bot:**
   ```bash
   python bot.py
   ```

2. **Make sure you have stalked players:**
   ```
   /stalk list
   ```
   
   If you don't have any, add yourself:
   ```
   /stalk add game_name:YourName tag_line:TAG
   ```

3. **Play a ranked game (or wait for a stalked player to finish one)**

4. **Wait 2-4 minutes** (bot checks every 2 minutes)

5. **Check the player's thread** - you should see:
   ```
   ✅ Victory - New Match Detected!
   Champion: Malzahar
   KDA: 8/3/12 (6.67)
   Duration: 32min
   📊 Rank Change: Silver IV 45 LP (+17 LP) 📈
   ```

6. **If someone gets promoted/demoted**, you'll see a separate message:
   ```
   🎉 PROMOTION! AlexTheSomething#2222 has been promoted to Silver III! 🎉
   ```

---

### **Feature 2: Clash Tournament Tracker**

Shows upcoming Clash tournaments with dates and times!

#### What It Does:
- Fetches Clash tournament schedules from Riot API
- Shows tournament names and dates
- Displays times in UTC
- Works for your configured region (EUN1 by default)

#### How to Test:

1. **Run the command:**
   ```
   /clash
   ```

2. **Expected Output (if Clash is active):**
   ```
   ⚔️ Upcoming Clash Tournaments
   2 tournament(s) scheduled for EUN1
   
   🏆 Clash Tournament Name
   • Feb 10 - 07:00 PM UTC
   • Feb 11 - 07:00 PM UTC
   • Feb 12 - 07:00 PM UTC
   
   📝 How to Join
   1. Open League of Legends client
   2. Click on Clash tab
   3. Create or join a team
   4. Register before the deadline!
   ```

3. **If No Clash is Scheduled:**
   ```
   ⚔️ Clash Tournaments
   No upcoming Clash tournaments scheduled at the moment.
   
   Check back later or visit the League client for updates!
   ```

---

## 🔍 What to Look For

### Rank Change Notifications:

✅ **LP Gains** - Should show "+X LP 📈" for wins  
✅ **LP Losses** - Should show "-X LP 📉" for losses  
✅ **Promotion Messages** - Separate embed with 🎉  
✅ **Demotion Messages** - Separate message with 😢  
✅ **Works for all stalked players** - Each player's thread gets updates  

### Clash Tracker:

✅ **Shows tournament names**  
✅ **Shows dates in UTC**  
✅ **Shows "How to Join" instructions**  
✅ **Handles no tournaments gracefully**  
✅ **Works with your region** (check config.py)  

---

## 🐛 Common Issues & Fixes

### Rank Changes Not Showing:

**Problem:** No "📊 Rank Change" field in match updates  
**Cause:** Player is unranked OR first match since tracking started  
**Solution:** 
- Make sure player has ranked games
- The first match after tracking starts won't show LP change (needs baseline)
- Second match onwards will show LP changes!

---

### Clash Shows Nothing:

**Problem:** Says "No upcoming Clash tournaments"  
**Cause:** Clash might not be active in your region right now  
**Solution:** 
- This is normal! Clash runs on specific weekends
- Check the League client to confirm
- Try again when Clash is announced

---

### Promotion/Demotion Not Detected:

**Problem:** Player ranked up but no special message  
**Cause:** Needs 2 matches to detect rank change  
**Solution:**
- First match: Sets baseline rank
- Second match: Shows LP change
- Third match (if promoted): Shows promotion message!

---

## 📊 Expected Behavior Examples

### Example 1: First Match After Tracking
```
✅ Victory - New Match Detected!
Champion: Malzahar
KDA: 8/3/12 (6.67)
Duration: 32min
(No rank change shown yet - establishing baseline)
```

### Example 2: Second Match (Win)
```
✅ Victory - New Match Detected!
Champion: Zed
KDA: 10/2/5 (7.5)
Duration: 28min
📊 Rank Change: Silver IV 62 LP (+18 LP) 📈
```

### Example 3: Loss
```
❌ Defeat - New Match Detected!
Champion: Yasuo
KDA: 3/9/4 (0.78)
Duration: 35min
📊 Rank Change: Silver IV 45 LP (-17 LP) 📉
```

### Example 4: Promotion
```
✅ Victory - New Match Detected!
Champion: Jinx
KDA: 12/3/8 (6.67)
Duration: 30min
📊 Rank Change: Silver III 0 LP (+19 LP) 📈

🎉 PROMOTION! AlexTheSomething#2222 has been promoted to Silver III! 🎉
```

---

## 🎮 Quick Test Checklist

- [ ] Bot starts without errors
- [ ] `/clash` command appears in command list
- [ ] `/clash` shows tournament data (or "none scheduled")
- [ ] Stalked player finishes a ranked match
- [ ] Match update appears in thread (2 min delay)
- [ ] LP change shows in match embed
- [ ] (If lucky) Promotion/demotion message appears
- [ ] No errors in console
- [ ] All data saves to `tracked_users.json`

---

## 🚀 Production Checklist

Before hosting 24/7:

- [ ] Test rank tracking with 2-3 matches
- [ ] Verify LP calculations are accurate
- [ ] Test `/clash` command
- [ ] Check console for errors
- [ ] Verify `tracked_users.json` updates correctly
- [ ] Test with multiple stalked players
- [ ] Push changes to GitHub ✅ (Already done!)

---

## 💡 Tips

1. **Testing Rank Changes:** Play ranked games on a tracked account, or track someone who plays frequently
2. **Fast Testing:** Set 2-3 active players to track - increases chances of catching matches
3. **Console Logs:** Watch for `[Monitor]` logs showing rank changes
4. **Data Persistence:** Check `data/tracked_users.json` - should have `last_rank` and `prev_last_rank` fields

---

## 🎉 You're All Set!

Your bot now has:
- ✅ Real-time LP tracking
- ✅ Promotion/demotion alerts
- ✅ Clash tournament schedules
- ✅ Complete stalking system
- ✅ Duo detection
- ✅ Live game monitoring

**Time to host it 24/7!** Check `HOSTING.md` for deployment options! 🚀

