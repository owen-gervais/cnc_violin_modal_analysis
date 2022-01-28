import os

f = open("test.gcode", "w")

points = [(140, 220)]

safe_z_max_retract = 'G38.3 Z100;\n'
safe_c_min_retract = 'G38.3 C-100;\n'
safe_z_homing = 'G28 Z;\n'
xyzc_homing = 'G28;\n'

system_dwell = 'G4 P3000;\n'

hammer_trigger_high = 'M42 P47 S255;\n'
hammer_trigger_low =  'M42 P47 S0;\n'

y_backup_offset = 180
z_probe_offset = -18

for point in points:
    x = point[0]
    y = point[1]
 
    f.write(safe_z_max_retract)
    f.write(safe_c_min_retract)
    f.write(xyzc_homing)
    f.write(safe_z_max_retract)

    f.write('G0 X{}\n'.format(point[0]))
    f.write('G0 C90\n')
    f.write('G0 Y{}\n'.format(point[1]))

    f.write(safe_z_homing)

    f.write('G0 Y{}\n'.format(point[1]-y_backup_offset))
    f.write('G0 Z{}\n'.format(z_probe_offset))

    f.write(system_dwell)
    f.write(hammer_trigger_high)
    f.write(system_dwell)
    f.write(hammer_trigger_low)

f.close()
