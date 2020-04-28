function test_python_f_interp

arts_sims = '~/Dendrite/Projects/AWS-325GHz/test_sample/c_of_2015_219_13.nc';
pyth_tb   = '~/Dendrite/Projects/AWS-325GHz/test_sample/TB.nc';

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

imeth = 'spline';


Y   = ncread( arts_sims, 'y_aws' ); %[stokes,f,angle,case]
TB0 = ncread( pyth_tb, 'TB' )'; %[case]

keyboard

TB = zeros( size(TB0) );

% Window channels
ind       = [find(f==89e9) find(f==165.5e9) find(f==229e9)];
out       = [1 2 8];
TB(out,:) = squeeze( Y(1,ind,1,:) - Y(2,ind,end,:) );

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
%TB(out,:) = squeeze( Y(1,ind,1,:) - Y(2,ind,end,:) );;


% 325 GHz
%
% Lower band
chs325    = channels_aws325ghz( '3' );
ind       = find( f>310e9 & f<325.15e9 );
f_fine    = min(chs325(:)) : 5e6 : max(chs325(:));
TB_fine   = interp1( f(ind), squeeze(Y(1,ind,end,:)-Y(2,ind,end,:)), f_fine, ...
                     imeth, 'extrap' ) ;
TB_low    = apply_channels( f_fine, TB_fine, chs325 );
%TB_low    = squeeze( Y(1,10:12,1,:) - Y(2,10:12,end,:) );;
%
% Upper band
chs325    = sort( 2*325.15e9-chs325, 2 );
ind       = find( f>325.15e9 );
f_fine    = min(chs325(:)) : 5e6 : max(chs325(:));
TB_fine   = interp1( f(ind), squeeze(Y(1,ind,end,:)-Y(2,ind,end,:)), f_fine, ...
                     imeth, 'extrap' ) ;
TB_upp    = apply_channels( f_fine, TB_fine, chs325 );
%TB_upp    = squeeze( Y(1,17:-1:15,1,:) - Y(2,17:-1:15,end,:) );;
%
out       = 9 : 11;
TB(out,:) = ( TB_low + TB_upp ) /2;

ic = 3;
h=plot(TB(8+ic,:),TB(3+ic,:),'.',TB0(8+ic,:),TB0(3+ic,:),'.',[250 290],[250 290],'k-');
xlabel('AWS42')
ylabel('AWS34')
legend(h(1:2),'Matlab','Python')


