from gpxpy import parse as gpx_parse, gpx, geo

init_gpx = gpx_parse(open("../../T-rid to Moab/Telluride_Moab_GPS_2021.gpx", "r"))
for track in init_gpx.tracks:
    track_name = track.name.replace("Day ", "D").replace("sanjuanhuts", "").rstrip()
    track.name = track_name
    new_gpx = gpx.GPX()
    new_gpx.tracks.append(track)
    track.extensions = []  # extensions are dumb, remove

    for waypoint in init_gpx.waypoints:
        location = geo.Location(
            waypoint.latitude, waypoint.longitude, waypoint.elevation
        )
        nearest = track.get_nearest_location(location)
        if nearest:
            dist_between_points = geo.distance(
                waypoint.latitude,
                waypoint.longitude,
                waypoint.elevation,
                nearest.location.latitude,
                nearest.location.longitude,
                nearest.location.elevation,
            )

            if dist_between_points < 45:  # distance in meters ~ 150 feet from the main trail
                waypoint.remove_time()
                waypoint.comment = None
                waypoint.extensions = []  # fucks up the wahoo
                waypoint.description = waypoint.name
                new_gpx.waypoints.append(waypoint)
    filename = track_name.replace(":", "").replace(" ", "")
    with open(f"output/{filename}.gpx", "w") as new_file:
        new_file.write(new_gpx.to_xml())
