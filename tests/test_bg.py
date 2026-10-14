from core.story_engine import StoryManager

story = StoryManager()
story.current_beat = 1

beat_str = str(story.current_beat)
bg = story.campaign_data.get(beat_str, {}).get("bg_image")
print(f"Beat {story.current_beat} BG: {bg}")

story.current_beat = 15
beat_str = str(story.current_beat)
bg = story.campaign_data.get(beat_str, {}).get("bg_image")
print(f"Beat {story.current_beat} BG: {bg}")

