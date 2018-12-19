from .channel import Channel
import re

class M3u:

    def parse(self, filename):

        channels = []

        # read file line by line
        with open(filename) as file:
            for line in file:

                # if first line, skip it
                if line == '#EXTM3U': continue

                # if is url, add to last one channel
                if line.startswith('#EXTINF:-1') == False:
                    if len(channels) == 0 : continue

                    last_channel = channels[-1]

                    last_channel.url = line

                # if its channel info line
                else:

                    # Split by space to get channel informations
                    info = re.findall(r'"(.*?)"', line)

                    # Parse major groups
                    tvgId = info[0]
                    tvgName = info[1]
                    tvgLogo = info[2]
                    groupTitle = info[3]

                    # Parse channel name
                    name = line.split(',')[-1].replace('\n', '')

                    # Add channel instance to array
                    channels.append(Channel(
                        tvgId,
                        tvgName,
                        tvgLogo,
                        groupTitle,
                        name
                    ))

        return channels

    def buildFile(self, channels, outputFile):

        str = "#EXTM3U\n"

        for channel in channels:

            str += '#EXTINF:-1 tvg-ID="' + channel.tvgId + '" tvg-name="' + channel.tvgName + '" tvg-logo="' + channel.tvgLogo + '" group-title="' + channel.groupTitle + '",' + channel.name + '\n'
            str += channel.url

        with open(outputFile, 'a') as file:
            file.write(str)