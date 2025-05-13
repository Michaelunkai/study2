obs = obslua

-- User-configurable variables.
local mp3_file_path = "C:\\study\\hosting\\recording\\obs\\super_pac_man_intro.mp3"
local removal_delay_ms = 10000  -- Delay (in milliseconds) after which the temporary media source is removed.

-- Global variables to hold references to the created objects.
local intro_source = nil
local intro_scene = nil
local intro_scene_item = nil

-- Script description shown in OBS's Scripts dialog.
function script_description()
    return "When recording starts, this script will play a background MP3 (set by mp3_file_path) by temporarily adding a hidden media source to your current scene."
end

-- This callback is invoked on OBS frontend events.
function on_event(event)
    if event == obs.OBS_FRONTEND_RECORDING_STARTED then
        obs.script_log(obs.LOG_INFO, "Recording started – playing intro MP3.")
        play_intro_mp3()
    end
end

-- Create a temporary media source for the MP3 and add it to the current scene.
function play_intro_mp3()
    -- Create settings for the media source.
    local settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "local_file", mp3_file_path)
    -- Optionally, you can adjust properties like "looping" (set to false so it plays just once).
    obs.obs_data_set_bool(settings, "looping", false)

    -- Create the media source using the "ffmpeg_source" (which supports audio files).
    intro_source = obs.obs_source_create("ffmpeg_source", "intro_source", settings, nil)
    obs.obs_data_release(settings)

    if intro_source == nil then
        obs.script_log(obs.LOG_WARNING, "Failed to create media source for the MP3 file!")
        return
    end

    -- Get the current scene so that the source can be added.
    intro_scene = obs.obs_frontend_get_current_scene()
    if intro_scene == nil then
        obs.script_log(obs.LOG_WARNING, "No current scene found!")
        obs.obs_source_release(intro_source)
        return
    end

    -- Add the media source to the current scene.
    intro_scene_item = obs.obs_scene_add(intro_scene, intro_source)
    if intro_scene_item == nil then
        obs.script_log(obs.LOG_WARNING, "Failed to add the media source to the current scene!")
        obs.obs_source_release(intro_source)
        obs.obs_source_release(intro_scene)
        return
    end

    -- Hide the scene item so that only the audio plays.
    obs.obs_sceneitem_set_visible(intro_scene_item, false)

    -- Restart the media source so it plays from the beginning.
    obs.obs_source_media_restart(intro_source)

    -- Schedule removal of the temporary source after the defined delay.
    obs.timer_add(remove_intro_source, removal_delay_ms)

    -- Release our references (the scene holds its own reference to the source/item).
    obs.obs_source_release(intro_source)
    obs.obs_source_release(intro_scene)
end

-- Timer callback to remove the temporary media source from the scene.
function remove_intro_source()
    if intro_scene and intro_scene_item then
        obs.obs_scene_remove(intro_scene, intro_scene_item)
        obs.script_log(obs.LOG_INFO, "Removed temporary intro media source.")
    end
    -- Remove the timer so it does not repeat.
    obs.timer_remove(remove_intro_source)
    -- Clear global variables.
    intro_source = nil
    intro_scene = nil
    intro_scene_item = nil
end

-- When the script is loaded, register for frontend events.
function script_load(settings)
    obs.obs_frontend_add_event_callback(on_event)
end
