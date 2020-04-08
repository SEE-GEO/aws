% FORMAT Q = q_basic(atm,f_grid,r_surface)
%
%   Returns a Q matching the project absorption settings and using a Fascod
%   climatology. 
%
% OUT   Q           A complete Q
% IN    atm         Climatlogy to use: 'tro', 'mls', 'mlw', 'sas' and 'saw'
%       f_grid      As the WSV.
%       r_surface   Surface reflectivity, a scalar.

% 2020-03-29   Patrick Eriksson

function Q = q_basic(atm,f_grid,r_surface)


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
Q.SENSOR_LOS            = 155;
%
Q.F_GRID                = vec2col( f_grid );
Q.P_GRID                = z2p_simple( -500:500:50e3 )';


%- External version
%
Q.INCLUDES              = { fullfile( 'ARTS_INCLUDES', 'general.arts' ), ...
                            fullfile( 'ARTS_INCLUDES', 'agendas.arts' ), ...
                            fullfile( fileparts(pwd), 'SetupTesting', ..., 
                                                      'include_mpm89_cont.arts' ), ...
                            fullfile( 'ARTS_INCLUDES', 'planet_earth.arts' ) };
%
Q.ABSORPTION            = 'OnTheFly';
Q.ABS_SPECIES(1).TAG{1} = 'N2-SelfContStandardType';
Q.ABS_SPECIES(2).TAG{1} = 'H2O,H2O-MPM89';
Q.ABS_SPECIES(3).TAG{1} = 'O3';
Q.ABS_LINES_FORMAT      = 'XML';
Q.ABS_LINES             = fullfile( fileparts(pwd), 'SetupTesting', ...
                                    { 'abs_lines_h2o_rttov.xml', ...
                                      'abs_lines_o3_afew.xml' } );
