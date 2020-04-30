function test_python_f_interp

%- Hard-coded settings
%
imeth = 'spline';
%
arts_sims = '~/Dendrite/Projects/AWS-325GHz/test_sample/c_of_2015_219_13.nc';
pyth_tb   = '~/Dendrite/Projects/AWS-325GHz/test_sample/TB.nc';
%
f = [89.0000
  165.5000
  175.8110
  177.4360
  179.0610
  180.6860
  182.3110
  229.0000
  316.6500
  318.5250
  320.4000
  322.2750
  324.1500
  326.1500
  328.0250
  329.9000
  331.7750
  333.6500] * 1e9;


%- Read data and create Matlab TB variable
%
Y   = ncread( arts_sims, 'y_aws' ); %[stokes,f,angle,case]
TB0 = ncread( pyth_tb, 'TB' )'; %[case]
%                                
TB = zeros( size(TB0) );


% Window channels
ind       = [find(f==89e9) find(f==165.5e9) find(f==229e9)];
out       = [1 2 8];
TB(out,:) = squeeze( Y(1,ind,end,:) - Y(2,ind,end,:) );


% 183 GHz
%
chs183  = channels_fixed;
%
ind       = find( f>170e9 & f<183e9 );
out       = 3:7;
f_fine    = min(chs183(:)) : 5e6 : max(chs183(:));
TB_fine   = interp1( f(ind), squeeze(Y(1,ind,end,:)-Y(2,ind,end,:)), f_fine, ...
                     imeth, 'extrap' ) ;
TB(out,:) = apply_channels( f_fine, TB_fine, chs183 );


% 325 GHz
%
% Lower band
f0        = 325.15e9;
chs325    = channels_aws325ghz( '3' );
n325      = size( chs325, 1 );
ind       = find( f>310e9 & f<f0 );
f_fine    = min(chs325(:)) : 5e6 : max(chs325(:));
TB_fine   = interp1( f(ind), squeeze(Y(1,ind,end,:)-Y(2,ind,end,:)), f_fine, ...
                     imeth, 'extrap' ) ;
TB_low    = apply_channels( f_fine, TB_fine, chs325 );
%
% Upper band
chs325    = sort( 2 * f0 - chs325, 2 );
ind       = find( f>f0 );
f_fine    = min(chs325(:)) : 5e6 : max(chs325(:));
TB_fine   = interp1( f(ind), squeeze(Y(1,ind,end,:)-Y(2,ind,end,:)), f_fine, ...
                     imeth, 'extrap' ) ;
TB_upp    = apply_channels( f_fine, TB_fine, chs325 );
%
out       = 8 + (1 : n325);
TB(out,:) = ( TB_low + TB_upp ) /2;


if 1
  % 183 vs 325 Ghz plot  
  ic = 2;
  h=plot(TB(8+ic,:),TB(3+ic,:),'.',[240 290],[240 290],'k-');
  xlabel( sprintf('AWS-4%d',ic) )
  ylabel( sprintf('AWS-3%d',ic+2) )
 legend(h(1:2),'Matlab','Python')

else
  % Agreement beween matalba and python plots
  close all
  for i = 11 : -1 : 1
    figure(i)
    plot( TB(i,:)-TB0(i,:) )
    xlabel( 'Case index' )
    ylabel( 'Matlab-Python [K]' )
    title( sprintf( 'Channel %d', i ) );
  end
end
