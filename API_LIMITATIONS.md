# ⚠️ Current API Limitations

## Riot API Issue - Missing Summoner ID

### Problem
The Riot Games API is currently not returning the `id` field when requesting summoner data via the `/lol/summoner/v4/summoners/by-puuid/{puuid}` endpoint.

**Expected Response:**
```json
{
  "id": "encrypted_summoner_id",
  "accountId": "encrypted_account_id", 
  "puuid": "...",
  "profileIconId": 6022,
  "revisionDate": 1761157269482,
  "summonerLevel": 105
}
```

**Actual Response:**
```json
{
  "puuid": "...",
  "profileIconId": 6022,
  "revisionDate": 1761157269482,
  "summonerLevel": 105
}
```

### Impact

The missing `id` field affects the following features:

#### ❌ Disabled Commands:
- `/rank` - Cannot fetch ranked data (needs summoner ID for `/lol/league/v4/entries/by-summoner/{id}`)
- `/livegame` - Cannot check spectator data (needs summoner ID for `/lol/spectator/v5/active-games/by-summoner/{id}`)

#### ❌ Disabled Monitoring Features:
- Live game detection - Cannot detect when players start games
- Rank tracking in threads - Initial player threads don't show rank

#### ✅ Working Features:
- `/summoner` - Basic player info (uses PUUID)
- `/recentmatches` - Match history (uses PUUID)
- `/championmastery` - Top champions (uses PUUID)
- `/rotation` - Free champion rotation (no player data needed)
- `/compare` - Compare players (uses working endpoints)
- **Match monitoring** - Detects new matches (uses PUUID)
- **Duo detection** - Tracks recurring teammates (uses PUUID)
- All stalking/tracking commands work

### Workaround

The code has been modified to gracefully handle the missing `id` field:

1. **Rank functions return empty arrays** instead of crashing
2. **Live game functions return `None`** instead of erroring
3. **Disabled commands are commented out** but preserved for future use
4. **Monitoring continues working** for match tracking and duo detection

### When Will This Be Fixed?

This appears to be either:
- A Riot API bug/regression
- A limitation of Development API keys
- A regional issue

**Potential Solutions:**
1. **Wait for Riot to fix** - This may be a temporary API issue
2. **Apply for Production API key** - May have full data access
3. **Use different region** - Issue may be region-specific

### Re-enabling Features

When the API is fixed, simply uncomment the disabled code:

**In `commands/rank.py`:**
- Uncomment all imports and the command definition

**In `commands/livegame.py`:**
- Uncomment all imports and the command definition

**In `commands/track.py`:**
- Uncomment rank embed creation (lines ~167-170)
- Uncomment rank embed in thread creation (lines ~184, ~202)
- Uncomment live game checking (line ~407)

**In `commands/help.py`:**
- Remove the ~~strikethrough~~ from disabled commands

No other changes needed - the bot will work immediately once Riot fixes their API!

---

**Last Updated:** October 22, 2025  
**Status:** Monitoring for Riot API updates

