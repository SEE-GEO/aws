function setup_o2_n2(atm,f_grid,r_surface)


%= Expand atm settings
%
switch lower(atm)
 case 'tro'
  atmlong = 'tropical';
 case 'mls'
  atmlong = 'midlatitude-summer';
 case 'mlw'
  atmlong = 'midlatitude-winter';
 case 'sas'
  atmlong = 'subarctic-summer';
 case 'saw'
  atmlong = 'subarctic-winter';
 otherwise
  error( 'Unknown option for *atm*.' );
end


%= Common settings
%
Q  = qarts;
%
Q.CLOUDBOX_DO           = false;
Q.J_DO                  = false;
Q.SENSOR_DO             = false;
%
Q.PPATH_AGENDA          = { 'ppath_agenda__FollowSensorLosPath'   };
Q.PPATH_STEP_AGENDA     = { 'ppath_step_agenda__GeometricPath'    };
Q.IY_SPACE_AGENDA       = { 'iy_space_agenda__CosmicBackground'   };
Q.IY_SURFACE_AGENDA     = { 'iy_surface_agenda__UseSurfaceRtprop' };
Q.IY_MAIN_AGENDA        = { 'iy_main_agenda__Emission'            };
Q.SURFACE_RTPROP_AGENDA = { ...
 'surface_rtprop_agenda__Specular_NoPol_ReflFix_SurfTFromt_field' };
%
Q.ATMOSPHERE_DIM        = 1;
%
Q.RAW_ATM_EXPAND_1D     = false;
Q.RAW_ATMOSPHERE        = fullfile( atmlab( 'ARTS_XMLDATA_PATH' ), 'planets', ...
                                    'Earth', 'Fascod', atmlong, atmlong );
%
Q.ABSORPTION            = 'OnTheFly';
%
Q.Z_SURFACE             = 0;
Q.WSMS_AT_START{end+1}  = sprintf( ...
    'VectorSet( surface_scalar_reflectivity, [%.4f] )', r_surface );
%
Q.STOKES_DIM            = 1;
Q.IY_UNIT               = 'PlanckBT';
Q.PPATH_LMAX            = -1;
Q.YCALC_WSMS            = { 'yCalc' };
%
Q.SENSOR_POS            = 600e3;
Q.SENSOR_LOS            = 170;
%
Q.F_GRID                = vec2col( f_grid );
Q.P_GRID                = z2p_simple( -500:250:50e3 )';


%- Full version
%
Q.INCLUDES              = { fullfile( 'ARTS_INCLUDES', 'general.arts' ), ...
                            fullfile( 'ARTS_INCLUDES', 'agendas.arts' ), ...
                            fullfile( pwd, 'include_mpm89_cont.arts' ), ...
                            fullfile( 'ARTS_INCLUDES', 'planet_earth.arts' ) };
%
Q.ABS_SPECIES(1).TAG{1}   = 'N2-SelfContStandardType';
Q.ABS_SPECIES(2).TAG{1}   = 'O2-PWR98';
Q.ABS_SPECIES(3).TAG{1}   = 'H2O,H2O-MPM89';
Q.ABS_LINES_FORMAT        = 'ARTSCAT';
Q.ABS_LINES               = fullfile( pwd, 'lines_rttov.xml' );
Q.ABS_LINESHAPE           = 'VP';
Q.ABS_LINESHAPE_FACTOR    = 'VVW';
Q.ABS_LINESHAPE_CUTOFF    = -1;
Q.ABS_LINESHAPE_MIRRORING = 'Lorentz';
%
y1 = arts_y( Q );


%- Ignore N2
%
Q.ABS_SPECIES(1).TAG{1}   = 'N2';
%
y2 = arts_y( Q );


%- Ignore 02
%
Q.ABS_SPECIES(1).TAG{1}   = 'N2-SelfContStandardType';
Q.ABS_SPECIES(2).TAG{1}   = 'O2';
%
y3 = arts_y( Q );


%- Plot results
%
plot( f_grid/1e9, y2-y1, f_grid/1e9, y3-y1 );
%
xlabel( 'Frequency [GHz]' );
ylabel( 'Difference [K]' );
legend( 'Ignore N2', 'Ignoring O2' );


