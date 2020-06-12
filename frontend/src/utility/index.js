
const GMAPS_BASE_URL = "https://www.google.com/maps/dir/?api=1";

/**
 * Generate google maps url based on waypoints for live directions
 */
export function generateMapURL(waypoints, waypointCount) {
    const startIndex = 0;
    const endIndex = waypoints.length - 1;
    
    // Get origin waypoint
    const origin = "&origin=" + waypoints[startIndex].lat.toString() + "," + waypoints[startIndex].lng.toString()

    // Get destination waypoint
    const end = "&destination=" + waypoints[endIndex].lat.toString() + "," + waypoints[endIndex].lng.toString() + "&travelmode=walking";

    
    // For loop incrementer
    let inc = Math.floor(waypoints.length / waypointCount);
    let steps = "&waypoints=";
    let i;

    // Get intermediate waypoints, only every waypointCount'th waypoint is included
    for(i = 1; i < waypoints.length-1; i=i+inc) {

        // Add waypoint to waypoints string
        steps += waypoints[i].lat.toString() + "," + waypoints[i].lng.toString()

        // If we arent at the end, add | for AND
        if(i !== waypoints.length-2) {
            steps += "|"
        }
    }

    // Return URL
    const url = GMAPS_BASE_URL + origin + steps.substring(0, steps.length-1) + end;
    return url;
}