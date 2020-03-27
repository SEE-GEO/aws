% CONVERT_MPM89_LINES
%
% Converts line data from MPM89 to a ARTSCAT3 format. The result is written
% directly to the file: lines_mpm89.xml
%
% If the optional argument *do_rttov* is set, some data are modified in
% order to what is used in RTTOV and the result is written to: lines_rttov.xml
%
% Absorptivity (in 1/m) in ARTS for one transition is
% alpha = i * (p*v)/(k_b*T) * Q(T0)/Q(T) * (exp(-L/(k_b*T))-exp(-U/(k_b*T)))/
%         (exp(-L/(k_b*T))-exp(-U/(k_b*T))) * S_0 * F(f,f0)
% where i is the isotopolgue fraction, v is (full) VMR value of the species 
% and for the rest see ARTS1 paper (Buehler et al, 2005)
%
% Absorptivity (in 1/m) in MPM89 for one transition is
% alpha = 1e-3 * z * 0.1820 * f * b_1 * e * th^3.5 * exp(b1*(1-th)) * F'
% where the factor 1e-3 is due to usage of non-SI units, z is the conversion
% factor from dB/km to 1/m, th=(300/T) and for the rest see the MPM89 paper.
% Note that MPM89 line shape, F', is defined such that (pi*f)/f0 * F' = F.
%
% By analysing the temperature dependency of the (total) absorption, 
% it is found that th^2.5 * exp(b1*(1-th)) must be equal to
% Q(T0)/Q(T) * (exp(-L/(k_b*T))-exp(-U/(k_b*T)))/(exp(-L/(k_b*T))-exp(-U/(k_b*T)))
% By testing it was found that MPM must assume that Q(T) follows th^1.5,
% which is the standard approxmation for non-linear triatomic molecules.
% The transitions lower energy state is below derived by solving 
% th*exp(b1*(1-th)) =
% (exp(-L/(k_b*T))-exp(-U/(k_b*T)))/(exp(-L/(k_b*T))-exp(-U/(k_b*T)))
% for T=200K.
%
% By rearrangement of remaining terms, it is found that (T0=300K):
% S0 = pi * k_b * T0 * z * 0.1820e4 * i * v0 * b_1; 
%
% Using the produced linefile and the hard-coded MPM89 agrees inside 0.02K
% for satellite view, except for 448 GHz where deviations around 0.1 K are
% found? Not clarified why.  
%
% FORMAT convert_mpm89_lines(do_rttov)

% 2019-12-27 Patrick Eriksson


function convert_mpm89_lines(do_rttov)
%
if nargin == 0, do_rttov = false; end


% Line data from continuua.cc: 
L = {
      {22.235080, 0.1090, 2.143, 28.11, 0.69, 4.80, 1.00},
      {67.813960, 0.0011, 8.735, 28.58, 0.69, 4.93, 0.82},
      {119.995940, 0.0007, 8.356, 29.48, 0.70, 4.78, 0.79},
      {183.310074, 2.3000, 0.668, 28.13, 0.64, 5.30, 0.85},
      {321.225644, 0.0464, 6.181, 23.03, 0.67, 4.69, 0.54},
      {325.152919, 1.5400, 1.540, 27.83, 0.68, 4.85, 0.74},
      {336.187000, 0.0010, 9.829, 26.93, 0.69, 4.74, 0.61},
      {380.197372, 11.9000, 1.048, 28.73, 0.69, 5.38, 0.84},
      {390.134508, 0.0044, 7.350, 21.52, 0.63, 4.81, 0.55},
      {437.346667, 0.0637, 5.050, 18.45, 0.60, 4.23, 0.48},
      {439.150812, 0.9210, 3.596, 21.00, 0.63, 4.29, 0.52},
      {443.018295, 0.1940, 5.050, 18.60, 0.60, 4.23, 0.50},
      {448.001075, 10.6000, 1.405, 26.32, 0.66, 4.84, 0.67},
      {470.888947, 0.3300, 3.599, 21.52, 0.66, 4.57, 0.65},
      {474.689127, 1.2800, 2.381, 23.55, 0.65, 4.65, 0.64},
      {488.491133, 0.2530, 2.853, 26.02, 0.69, 5.04, 0.72},
      {503.568532, 0.0374, 6.733, 16.12, 0.61, 3.98, 0.43},
      {504.482692, 0.0125, 6.733, 16.12, 0.61, 4.01, 0.45},
      {556.936002, 510.0000, 0.159, 32.10, 0.69, 4.11, 1.00},
      {620.700807, 5.0900, 2.200, 24.38, 0.71, 4.68, 0.68},
      {658.006500, 0.2740, 7.820, 32.10, 0.69, 4.14, 1.00},
      {752.033227, 250.0000, 0.396, 30.60, 0.68, 4.09, 0.84},
      {841.073593, 0.0130, 8.180, 15.90, 0.33, 5.76, 0.45},
      {859.865000, 0.1330, 7.989, 30.60, 0.68, 4.09, 0.84},
      {899.407000, 0.0550, 7.917, 29.85, 0.68, 4.53, 0.90},
      {902.555000, 0.0380, 8.432, 28.65, 0.70, 5.10, 0.95},
      {906.205524, 0.1830, 5.111, 24.08, 0.70, 4.70, 0.53},
      {916.171582, 8.5600, 1.442, 26.70, 0.70, 4.78, 0.78},
      {970.315022, 9.1600, 1.920, 25.50, 0.64, 4.94, 0.67},
      {987.926764, 138.0000, 0.258, 29.85, 0.68, 4.55, 0.90}};


% Other hard-coded data
kb           = constants( 'BOLTZMANN_CONST' );
h            = constants( 'PLANCK_CONST' );

% MPM's reference temperature
t0           = 300;

% Matches factor 0.1820 and some units conversions giving 1e-3
cfac         = 1e4 * (4*pi/constants('SPEED_OF_LIGHT')) * log10(exp(1));

% Conversion from dB/km to 1/m
dB_km_to_1_m = (1e-3 / (10.0 * log10(exp(1))) );

% Relative abundance of H2O-161
isocorr      = 1/.997317;     

% Start of output file
%
if do_rttov
  filename = 'lines_rttov.xml';
else
  filename = 'lines_mpm89.xml';
end
%
fid = fopen( filename, 'w' );
%
fprintf( fid, '<?xml version="1.0"?>\n' );
fprintf( fid, '<arts format="ascii" version="1">\n' );
fprintf( fid, '<ArrayOfLineRecord version="ARTSCAT-3" nelem="%d">\n', length(L) );


% Loop lines
%
for i = 1:length(L)

  v0     = L{i}{1} * 1e9;
  i0     = pi * kb * t0 * dB_km_to_1_m * cfac * isocorr * v0 * L{i}{2};

  % elow is calculated by 
  t      = 200;
  th     = 300/t;
  r      = th * exp( L{i}{3} * (1 - th ) );
  elow   = - log( r * (1-exp(-h*v0/t0/kb)) / (1-exp(-h*v0/t/kb)) ) * ...
           kb / (1/t - 1/t0);
  
  AGAM   = L{i}{4} * 1e3;
  SGAM   = L{i}{4} * L{i}{6} * 1e3; 
  AGAM_T = L{i}{5};
  SGAM_T = L{i}{7};

  if do_rttov
    if abs( v0 - 22.235e9 ) < 1e6
      AGAM = 26560;
    elseif abs( v0 - 183.310e9 ) < 1e6
      AGAM   = 29190;
      AGAM_T = 0.77; 
    end
  end
  
  fprintf( fid, ['@ H2O-161 %.8e 0 %e %.0f %e ', ...
                 '%.2f %.2f %.2f %.2f %.0f 0 ', ...
                 '-1 -1 -1 -1 -1 -1 -1\n'], ...
           v0, i0, t0, elow, AGAM, SGAM, AGAM_T, SGAM_T, t0 );

end

% End of file
%
fprintf( fid, '</ArrayOfLineRecord>\n' );
fprintf( fid, '</arts>\n' );
%
fclose(fid);
