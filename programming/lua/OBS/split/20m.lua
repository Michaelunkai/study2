obs = obslua
interval = 1200  -- 20 minutes in seconds

-- This function will be called every 20 minutes
function timer_callback()
    if obs.obs_frontend_recording_active() then
        obs.obs_frontend_recording_stop()
        -- Add a short delay (e.g., 2 seconds) before restarting
        obs.timer_add(start_recording, 2000)
    end
end

-- Function to start recording again
function start_recording()
    obs.obs_frontend_recording_start()
    obs.timer_remove(start_recording)
end

-- Called when the script is loaded
function script_load(settings)
    obs.timer_add(timer_callback, interval * 1000)  -- Convert seconds to milliseconds
end

-- Called when the script is unloaded
function script_unload()
    obs.timer_remove(timer_callback)
end
