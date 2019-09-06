---------------------------------------------
-- xACARS.lua                              --
-- Speed_Limit75                           --
--                                         --
-- This file is the bridge between X-Plane --
-- and xACARS. This file is for Linux.     --
---------------------------------------------

function joinPath(x, y) -- Joins the file path of file X and file Y.
    return x .. "\\" .. y
end

fileLoc = os.getenv('APPDATA')
fileLoc = joinPath(fileLoc, 'xACARS')
logMsg(fileLoc)
starting_time = os.clock()

function writeData(x, y)
    file = joinPath(fileLoc, 'input')
    file = joinPath(file, x .. '.txt')
    
    f = io.open(file, "w")
    io.output(f)
    io.write(tostring(y))
    io.close(f)
end

function refresh()
    if os.clock() < starting_time + 0.4 then -- Forces script to wait... 0.4 seconds. Should probably be removed.
        -- Latitude
        lat = LATITUDE
        writeData('lat', lat)

        -- Longitude
        lon = LONGITUDE
        writeData('lon', lon)

        -- Heading
        hdg = get("sim/cockpit2/gauges/indicators/compass_heading_deg_mag")
        writeData('heading', hdg)

        -- Vertical Speed
        vs = get("sim/cockpit2/gauges/indicators/vvi_fpm_pilot")
        vs = tostring(vs)
        if string.match(vs, "e") then
            vs = 0.0
        else
            vs = tonumber(vs)
            vs = vs * 1.94384
        end
        writeData("vs", vs)

        -- Altitude
        alt = get("sim/cockpit2/gauges/indicators/altitude_ft_pilot")
        writeData('altitude', alt)

        -- Ground Speed
        gs = get("sim/flightmodel/position/groundspeed")
        gs = tostring(gs)
        if string.match(gs, "e") then
            gs = 0.0
        else
            gs = tonumber(gs)
            gs = gs * 1.94384
        end
        writeData("gs", gs)

        -- Indicated Airspeed
        ias = get("sim/flightmodel/position/indicated_airspeed")
        writeData('IAS', ias)

        starting_time = os.clock()
    end
end

do_often("refresh()")