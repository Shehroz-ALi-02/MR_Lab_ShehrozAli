## Base Geometry & Hull Redesign 

Modification: Replaced the default cylinder shape with a low-profile, heavy-duty rectangular chassis footprint (0.6m × 0.45m × 0.15m).  

Purpose: Provides a realistic industrial look resembling modern AMRs (e.g., MiR or Clearpath platforms). This wide-base design maximizes surface area for carrying payload decks.

## Kinematic Alignment & Stability Fix 

Modification: Expanded the setup from a single caster to two identical caster wheels positioned at the front and rear centers (xyz="±0.22 0 -0.09").  

The Math Correction: Solved the robot tipping/clipping defect by perfectly balancing the ground contact point (z-axis alignment) relative to the base_link center

Drive Wheels: Radius (0.08m) + Joint Offset (-0.05m) = Ground level at -0.13.
Caster Wheels: Radius (0.04m) + Joint Offset (0.09m) = Ground level at -0.13.

Purpose: Ensures all four points of contact lie perfectly flat on the ground plane, preventing wobbling or unaligned physics loops in RViz and Gazebo.  

## Structural Layering & Multi-Stage Sensor Assembly

Modification: Layered a dedicated structural cargo sheet (top_plate) flushed to the upper edge of the chassis base. 

Modification: Built a two-stage elevated LiDAR array consisting of a structural lidar_tower neck and a primary blue lidar_sensor scanner head.  

Purpose: Elevating the LiDAR mimics a real-world AMR deployment, ensuring the sensor's scanning horizon clears any heavy cargo payloads placed on the top plate to allow unobstructed 360 deg environmental mapping. 

## Semantic Material Mapping

Modification: Implemented an industrial palette containing five discrete color profiles: industrial_yellow, dark_grey, light_grey, black, and sensor_blue.

Purpose: Enhances part distinction and asset readability during multi-link transformation testing inside RViz.
