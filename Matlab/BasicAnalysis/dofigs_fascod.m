%----------------------------------------------
%--- Compare bands
%----------------------------------------------

if 0

% Set channels
%
[chs183,ch229] = channels_fixed;
chs325         = channels_ici325ghz;
is_ici         = true;

% Results for r = 0
%
mkfigs_spectra_wfuns( 0, chs183, ch229, chs325, is_ici );
%
print -f1 fascod_tb_r000.pdf -dpdf


% Results for r = 0.5
%
mkfigs_spectra_wfuns( 0.5, chs183, ch229, chs325, is_ici );
%
print -f1 fascod_tb_r050.pdf -dpdf

% Results for r = 0.25
%
mkfigs_spectra_wfuns( 0.25, chs183, ch229, chs325, is_ici );
%
print -f3 fascod_wf_mls_025.pdf -dpdf
print -f8 fascod_tr_mls.pdf -dpdf


%----------------------------------------------
%--- Wfuns in wingds of 183 and 325 GHz
%----------------------------------------------

chs=325.15e9+[-11 -8;-10 -7;-9 -6;-8 -5]*1e9;
%
mkfigs_compare_chs( 'tro', 0.1, chs );
%
figure(1)
axis([-0.025 0 150 1000])
%
print -f1 fascod_wf_325l_tro.pdf -dpdf

chs=325.15e9+[8 11;7 10;6 9;5 8]*1e9;
%
mkfigs_compare_chs( 'tro', 0.1, chs );
%
figure(1)
axis([-0.025 0 150 1000])
%
print -f1 fascod_wf_325u_tro.pdf -dpdf

end


% 3-channel set
%
chs183 = channels_fixed;
ch229  = [];
chs325 = 325.15e9+[-8 -5; -4.8 -2.3; -2.2 -1.0]*1e9;
is_ici = false;
%
mkfigs_spectra_wfuns( 0.24, chs183, ch229, chs325, is_ici );
%
print -f2 fascod_3chopt_tro.pdf -dpdf
print -f4 fascod_3chopt_mlw.pdf -dpdf


% 4-channel set
%
chs325 = 325.15e9+[-8 -5.2; -5.0 -3.1; -3.0 -1.7; -1.6 -0.8]*1e9;
%
mkfigs_spectra_wfuns( 0.24, chs183, ch229, chs325, is_ici );
%
print -f2 fascod_4chopt_tro.pdf -dpdf
print -f4 fascod_4chopt_mlw.pdf -dpdf



!pdfcropbatch *.pdf


