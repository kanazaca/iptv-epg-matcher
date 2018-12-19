import difflib
import xml.etree.ElementTree as ET
from m3u.m3u import M3u

m3u = M3u()
channels = m3u.parse('lista1.m3u')

# Parse guide XML
tree = ET.parse('guide.xml')
root = tree.getroot()

for channel in root.findall('channel'):
    id = channel.get('id')

# Loop channels and find the best suit
for channel in channels:
    best = {
        'id' : '',
        'percentage' : 0
    }

    for el in root.findall('channel'):
        id = el.get('id')

        # just ignore if don't have more than 3 chars (i'm lazy)
        if len(id) <= 3:
            continue

        # Get similiarity
        percentage = difflib.SequenceMatcher(None, channel.name.lower(), id.lower() ).ratio()

        # If higher than what we have now, save it
        if percentage > best['percentage'] and percentage >= 0.50:
            best['id'] = id
            best['percentage'] = percentage
    
    # overwrite current tvgId
    channel.tvgId = best['id']

# Write file with epg
m3u.buildFile(channels, 'lista1_epg.m3u')