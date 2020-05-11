% Script to test adjust183.m
%
% FORMAT test_adjust183(i183,i325[,fignr,cs_reject,dTb_max_fit,noisy_fit,dTb_max_meas])

% 2020-05-11 Patrick Eriksson

function test_adjust183(i183,i325,varargin)
%
[fignr,cs_reject,dTb_max_fit,noisy_fit,dTb_max_meas] = optargs( varargin, ...
                                                  { 1, 0.5, 25, false, 25} );

% Input files
file1 = 'TB_AWS_m60_p60.nc';
file2 = 'TB_AWS_m60_p60_noise.nc';

% Could not read channel names for netCDF, so they are hard-coded
channels = { 'Ch21', 'Ch31', 'Ch32', 'Ch33', 'Ch34', 'Ch35', 'Ch36', ...
             'Ch4X', 'Ch41', 'Ch42', 'Ch43', 'Ch44' };

% Hard-coded settings
binstep = 0.2;   % Bin-size in distribution plot
ics     = 1;          % Index in in-data of clear and all-sky
ias     = 2;

% Read in simulations
TB0   = ncread( file1, 'TB' );
TB    = ncread( file2, 'TB_noise' );

% Reject a fraction of clear-sky 
%
ntot  = size( TB0, 1 );
ireje = abs( TB0(:,ias,i183)-TB0(:,ics,i183)) < 0.2 & rand(ntot,1)<cs_reject;
ntot  = ntot - sum(ireje);

% Select measurement data
%
tb183 = TB(:,ias,i183);
tb325 = TB(:,ias,i325);
%
im    = find( abs( tb183 - tb325 ) <= dTb_max_meas & ~ireje );
%
tb183 = tb183(im);
tb325 = tb325(im);

% Find index for data to use in fits
%
ifit  = find( abs( TB0(:,ias,i183)-TB0(:,ics,i183) ) <= dTb_max_fit );

% Estimate clear-sky values from measurements
%
if noisy_fit
  tb_cs_est = adjust183( TB(ifit,ics,i183), TB(ifit,ias,i183), TB(ifit,ias,i325), ...
                         tb183, tb325, std(TB(:,ics,i183)-TB0(:,ics,i183)) );
else
  tb_cs_est = adjust183( TB0(ifit,ics,i183), TB0(ifit,ias,i183), TB0(ifit,ias,i325), ...
                         tb183, tb325, std(TB(:,ics,i183)-TB0(:,ics,i183)) );
end

% Values to mimic Rekha et al
%
i229 = find( abs( TB0(:,ias,3) - TB0(:,ics,3) ) <= 4 & ~ireje );
cs_frac_removed229 = 0.5;  % Seems to be at least 50%

% Calculate PDFs
%
bins  = -20:binstep:5;
%
n1  = histc( mat2col(TB(~ireje,ics,i183)-TB0(~ireje,ics,i183)), bins );
n2a = histc( mat2col(TB(:,ias,i183)-TB0(:,ics,i183)), bins );
n2b = histc( mat2col(TB(im,ias,i183)-TB0(im,ics,i183)), bins );
n3  = histc( tb_cs_est - mat2col(TB0(im,ics,i183)), bins );
n4  = histc( mat2col(TB(i229,ias,i183)-TB0(i229,ics,i183)), bins );

figure(fignr)
semilogy( edges2grid(bins), n1(1:end-1)/(sum(n1)*binstep), ...
          edges2grid(bins), n2a(1:end-1)/(sum(n2a)*binstep), ...
          edges2grid(bins), n2b(1:end-1)/(sum(n2b)*binstep), ...
          edges2grid(bins), n3(1:end-1)/(sum(n3)*binstep), ...
          edges2grid(bins), n4(1:end-1)/(sum(n4)*binstep) );
axis( [min(bins) max(bins) 1e-4 1] )
xlabel( 'Deviation to noise free clear-sky [K]' );
ylabel( 'Occurence frequency [#/K]' );
title( sprintf( '%s/%s, fraction rejected: %.4f (%.4f)', ...
                channels{i183}, channels{i325}, ...
                1-length(tb183)/ntot, ...
                1-cs_frac_removed229*length(i229)/ntot ) );
legend( 'Noise', 'All measurements', 'Considered measurements', ...
        'After correction', 'Sreerekha et al', 'Location', 'NorthWest' )

print( sprintf('%s_%s.png',channels{i183}, channels{i325}), '-dpng' )
