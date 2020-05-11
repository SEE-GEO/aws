% ADJUST183   Cloud-correction of 13 GHz data
%
%   This is a potential algorith for the correction of 183 GHz using 325 GHz
%   data.
%
% FORMAT tb_cs_est = adjust183(
%                tb183_cs_sim,tb183_as_sim,tb325_as_sim,tb183,tb325,noise183)
%
% OUT  tb_cs_est     Estimated 183 GHz clear-sky values (a vector).
% IN   tb183_cs_sim  Simulated 183 GHz clear-sky values (a vector).
%      tb183_as_sim  Simulated 183 GHz all-sky values (a vector).
%      tb325_as_sim  Simulated 325 GHz all-sky values (a vector).
%      tb183         Measured 183 GHz values (a vector).
%      tb325         Measured 325 GHz values (a vector).
%      noise183      Mean noise of 183 GHz data (a scalar).

% 2020-05-11 Patrick Eriksson

function tb_cs_est = adjust183(tb183_cs_sim,tb183_as_sim,tb325_as_sim,tb183,tb325,noise183)

% Variables for fitting
x = tb325_as_sim - tb183_as_sim;
y = tb183_cs_sim - tb183_as_sim;

% Select subset to consider as cloudy for fitting and perform fit
%
dtb_fit = 0.2;
npoly   = 3;
%
cloudy0 = abs( y ) > 0.2;
%
p = polyfit( x(cloudy0), y(cloudy0), npoly );

% Init tb_cs_est 
%
tb_cs_est = tb183;

% Create boolen for cases considered as cloudy and shall be adjusted
% We do this by finding cases where adjustment is > 2 std of noise
% (Tested and 1 std gives quite similar results, except for Ch32)
xtest      = -10:0.2:5;
dtb        = interp1( polyval(p,xtest), xtest, 2*noise183 );
x_measured = tb325 - tb183;
cloudy     = x_measured < dtb;

% Apply adjustment
%
tb_cs_est(cloudy) = tb183(cloudy) + polyval( p, x_measured(cloudy) );

