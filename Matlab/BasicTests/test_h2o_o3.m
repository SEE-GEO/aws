% FORMAT [y1,y2,y3,y4] = test_h2o_o3(atm,f_grid,r_surface)
%
%   Returns spectra for some different absoprtion settings.
%
% OUT   y1          Tb for project settings
%       y2          Tb for extern version of MPM98-H2O
%       y3          Tb for hard-coded MPM89
%       y4          As y1 but some ozone lines included
% IN    atm         Climatlogy to use. See q_basic.
%       f_grid      As the WSV.
%       r_surface   Surface reflectivity, a scalar.

% 2020-03-29   Patrick Eriksson

function [y1,y2,y3,y4] = test_h2o_o3(atm,f_grid,r_surface)


Q = q_basic( atm, f_grid, r_surface );


%- Version mimicking RTTOV (used for the project)
%
tic
y1 = arts_y( Q );
toc
%
if nargout == 1, return, end


%- Version mimicking MPM89
%
Q.ABS_LINES               = fullfile( pwd, 'abs_lines_h2o_mpm89.xml' );
%
tic
y2 = arts_y( Q );
toc
%
if nargout == 2, return, end


%- Standard MPM89
%
Q.INCLUDES              = { fullfile( 'ARTS_INCLUDES', 'general.arts' ), ...
                            fullfile( 'ARTS_INCLUDES', 'agendas.arts' ), ...
                            fullfile( 'ARTS_INCLUDES', 'continua.arts' ), ...
                            fullfile( 'ARTS_INCLUDES', 'planet_earth.arts' ) };
%
Q.ABS_SPECIES(2).TAG{1} = 'H2O-MPM89';
Q.ABS_LINES_FORMAT      = 'None';
%
tic
y3 = arts_y( Q );
toc
%
if nargout == 3, return, end


%- RTTOV version + O3
%
Q = q_basic( atm, f_grid, r_surface );
%
Q.ABS_SPECIES(3).TAG{1}   = 'O3';
Q.ABS_LINES               = { fullfile( pwd, 'abs_lines_h2o_rttov.xml' ), ...
                              fullfile( pwd, 'abs_lines_o3_afew.xml' ) };
%
tic
%y4 = arts_y( Q );
y4=y1;
toc
%
if nargout == 4, return, end


%- Plot results
%
plot( f_grid/1e9, y2-y3, f_grid/1e9, y1-y2, f_grid/1e9, y4-y1 );
%
xlabel( 'Frequency [GHz]' );
ylabel( 'Difference [K]' );
legend( 'Line-by-line vs. MPM89', ...
        'RTTOV vs. line-by-line', ...
        'Include ozone lines' );