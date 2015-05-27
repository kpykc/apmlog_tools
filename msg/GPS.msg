# GPS
# https://github.com/diydrones/ardupilot/blob/master/libraries/DataFlash/DataFlash.h#L182
Header header
uint8 Status # uint8_t status;
             # uint32_t gps_week_ms (?)
uint16 Week  # uint16_t gps_week;
uint8 NSats  # uint8_t num_sats;
uint16 HDop  # uint16_t hdop;
int32 Lat    # int32_t  latitude;
int32 Lng    # int32_t  longitude;
int32 RelAlt # int32_t  rel_altitude;
int32 Alt    # int32_t  altitude; Altitude (AMSL, NOT WGS84), in meters * 1000 (positive for up)
uint32 Spd   # uint32_t ground_speed; (?)
int32 GCrs   # int32_t  ground_course; TODO: type?
float32 VZ   # float    vel_z; TODO: type?
uint32 T     # apm_time?  uint32_t apm_time;
