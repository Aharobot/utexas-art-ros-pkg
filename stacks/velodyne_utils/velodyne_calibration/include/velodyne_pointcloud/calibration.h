/**
 * \file  Calibration.h 
 *
 * \author  Piyush Khandelwal (piyushk@cs.utexas.edu)
 * Copyright (C) 2012, Austin Robot Technology, University of Texas at Austin
 *
 * License: Modified BSD License
 *
 * $ Id: 02/14/2012 11:25:34 AM piyushk $
 */

#ifndef CALIBRATION_CQUVIJWI
#define CALIBRATION_CQUVIJWI

namespace velodyne_pointcloud {

  /** \brief correction values for a single laser
   *
   * Correction values for a single laser (as provided by db.xml from veleodyne). Includes 
   * parameters for Velodyne HDL-64E S2.1
   * http://velodynelidar.com/lidar/products/manual/63-HDL64E%20S2%20Manual_Rev%20D_2011_web.pdf
   **/
  struct laser_correction {

    /** parameters in db.xml */
    float rot_correction;
    float vert_correction;
    float dist_correction;
    float vert_offset_correction;
    float horiz_offset_correction;
    int max_intensity;
    int min_intensity;
    float focal_distance;
    float focal_slope;

    /** cached values calculated when the calibration file is read */
    float cos_rot_correction;              ///< cached cosine of rot_correction
    float sin_rot_correction;              ///< cached sine of rot_correction
    float cos_vert_correction;             ///< cached cosine of vert_correction
    float sin_vert_correction;             ///< cached sine of vert_correction
  };

  /** \brief Calibration class storing entire configuration for the Velodyne */
  class Calibration {
  public:
    int num_lasers;
    float pitch;
    float roll;
    std::map<int, laser_correction> laser_corrections;
    bool initialized;

    Calibration();
    Calibration(const std::string& calibration_file) {
      read(calibration_file);
    }
    void read(const std::string& calibration_file);
    void write(const std::string& calibration_file);
    bool isInitialized();
  };
  
} /* velodyne_pointcloud */


#endif /* end of include guard: CALIBRATION_CQUVIJWI */


