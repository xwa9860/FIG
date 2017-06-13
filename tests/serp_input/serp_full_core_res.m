
% Increase counter:

if (exist('idx', 'var'));
  idx = idx + 1;
else;
  idx = 1;
end;

% Version, title and date:

VERSION                   (idx, [1: 14])  = 'Serpent 2.1.17' ;
TITLE                     (idx, [1:  8])  = 'FHR core' ;
INPUT_FILE_NAME           (idx, [1: 14])  = 'serp_full_core' ;
START_DATE                (idx, [1: 24])  = 'Sat Aug  1 16:07:41 2015' ;
COMPLETE_DATE             (idx, [1: 24])  = 'Sat Aug  1 18:14:29 2015' ;

% Run parameters:

POP                       (idx, 1)        = 200000 ;
CYCLES                    (idx, 1)        = 200 ;
SKIP                      (idx, 1)        = 500 ;
BATCH_INTERVAL            (idx, 1)        = 1 ;
SRC_NORM_MODE             (idx, 1)        = 2 ;
SEED                      (idx, 1)        = 1438470461 ;
UFS_MODE                  (idx, 1)        = 0 ;
UFS_ORDER                 (idx, 1)        = 1.00000;
NEUTRON_TRANSPORT_MODE    (idx, 1)        = 1 ;
PHOTON_TRANSPORT_MODE     (idx, 1)        = 0 ;
GROUP_CONSTANT_GENERATION (idx, 1)        = 1 ;
B1_CALCULATION            (idx, 1)        = 0 ;
B1_BURNUP_CORRECTION      (idx, 1)        = 0 ;
IMPLICIT_REACTION_RATES   (idx, 1)        = 1 ;
DEBUG                     (idx, 1)        = 0 ;
CPU_TYPE                  (idx, [1: 41])  = 'Intel(R) Xeon(R) CPU E5-2670 v2 @ 2.50GHz' ;
CPU_MHZ                   (idx, 1)        = 1046.0 ;

% Optimization:

OPTIMIZATION_MODE         (idx, 1)        = 4 ;
RECONSTRUCT_MICROXS       (idx, 1)        = 1 ;
RECONSTRUCT_MACROXS       (idx, 1)        = 1 ;
MG_MAJORANT_MODE          (idx, 1)        = 0 ;

% Parallelization:

MPI_TASKS                 (idx, 1)        = 1 ;
OMP_THREADS               (idx, 1)        = 20 ;
MPI_REPRODUCIBILITY       (idx, 1)        = 0 ;
OMP_REPRODUCIBILITY       (idx, 1)        = 1 ;
OMP_HISTORY_PROFILE       (idx, [1:  20]) = [  9.71282E-01  1.03289E+00  1.02666E+00  9.72886E-01  9.61205E-01  1.03301E+00  9.73820E-01  9.68390E-01  1.03013E+00  9.70539E-01  9.72151E-01  1.02997E+00  1.02690E+00  1.02965E+00  1.03345E+00  9.67800E-01  1.02345E+00  9.72162E-01  9.74333E-01  1.02933E+00  ];
SHARE_BUF_ARRAY           (idx, 1)        = 0 ;
SHARE_RES2_ARRAY          (idx, 1)        = 1 ;

% File paths:

XS_DATA_FILE_PATH         (idx, [1: 71])  = '/global/home/groups/ac_nuclear/serpent/xsdata/endfb7/sss_endfb7u.xsdata' ;
DECAY_DATA_FILE_PATH      (idx, [1:  3])  = 'N/A' ;
SFY_DATA_FILE_PATH        (idx, [1:  3])  = 'N/A' ;
NFY_DATA_FILE_PATH        (idx, [1:  3])  = 'N/A' ;
BRA_DATA_FILE_PATH        (idx, [1:  3])  = 'N/A' ;

% Collision and reaction sampling (neutrons/photons):

MIN_MACROXS               (idx, [1:   4]) = [  1.49368E-01 0.0E+00  0.00000E+00 0.0E+00 ];
DT_THRESH                 (idx, [1:  2])  = [  9.00000E-01  9.00000E-01 ];
ST_FRAC                   (idx, [1:   4]) = [  6.68522E-02 0.00026  0.00000E+00 0.0E+00 ];
DT_FRAC                   (idx, [1:   4]) = [  9.33148E-01 1.9E-05  0.00000E+00 0.0E+00 ];
DT_EFF                    (idx, [1:   4]) = [  3.42653E-01 4.9E-05  0.00000E+00 0.0E+00 ];
IFC_COL_EFF               (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
REA_SAMPLING_EFF          (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
REA_SAMPLING_FAIL         (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
ETTM_SAMPLING_EFF         (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_COL_EFF               (idx, [1:   4]) = [  3.46249E-01 4.9E-05  0.00000E+00 0.0E+00 ];
ETTM_MAJORANT_FAIL        (idx, 1)        =  0.00000E+00 ;
ETTM_LIMITS_FAIL          (idx, [1:  2])  = [  0.00000E+00  0.00000E+00 ];
AVG_TRACKS                (idx, [1:   4]) = [  1.89266E+02 0.00013  0.00000E+00 0.0E+00 ];
AVG_REAL_COL              (idx, [1:   4]) = [  1.89206E+02 0.00013  0.00000E+00 0.0E+00 ];
AVG_VIRT_COL              (idx, [1:   4]) = [  3.57240E+02 0.00018  0.00000E+00 0.0E+00 ];
AVG_SURF_CROSS            (idx, [1:   4]) = [  3.60083E+01 0.00014  0.00000E+00 0.0E+00 ];

% Run statistics:

CYCLE_IDX                 (idx, 1)        = 200 ;
SOURCE_NEUTRONS           (idx, 1)        = 40000322 ;
MEAN_POP_SIZE             (idx, [1:  2])  = [  2.00002E+05 0.00024 ];
MEAN_POP_WGT              (idx, [1:  2])  = [  2.00002E+05 0.00024 ];
SIMULATION_COMPLETED      (idx, 1)        = 1 ;

% Running times:

TOT_CPU_TIME              (idx, 1)        =  2.51474E+03 ;
RUNNING_TIME              (idx, 1)        =  1.26801E+02 ;
INIT_TIME                 (idx, 1)        =  1.04690E+00 ;
PROCESS_TIME              (idx, [1:  2])  = [  7.38167E-02  7.38167E-02 ];
TRANSPORT_CYCLE_TIME      (idx, [1:  3])  = [  1.25680E+02  1.25680E+02  0.00000E+00 ];
BURNUP_CYCLE_TIME         (idx, [1:  2])  = [  0.00000E+00  0.00000E+00 ];
BATEMAN_SOLUTION_TIME     (idx, [1:  2])  = [  0.00000E+00  0.00000E+00 ];
MPI_OVERHEAD_TIME         (idx, [1:  2])  = [  0.00000E+00  0.00000E+00 ];
ESTIMATED_RUNNING_TIME    (idx, [1:  2])  = [  1.26800E+02  0.00000E+00 ];
CPU_USAGE                 (idx, 1)        = 19.83223 ;
TRANSPORT_CPU_USAGE       (idx, [1:   2]) = [  1.99913E+01 0.00022 ];
OMP_PARALLEL_FRAC         (idx, 1)        =  9.73725E-01 ;
OMP_AMDAHL_MAX            (idx, 1)        = 13.34 ;

% Memory usage:

AVAIL_MEM                 (idx, 1)        = 64498.02 ;
ALLOC_MEMSIZE             (idx, 1)        = 19940.10;
MEMSIZE                   (idx, 1)        = 18767.94;
XS_MEMSIZE                (idx, 1)        = 16998.23;
MAT_MEMSIZE               (idx, 1)        = 653.46;
RES_MEMSIZE               (idx, 1)        = 1.54;
MISC_MEMSIZE              (idx, 1)        = 1114.71;
UNKNOWN_MEMSIZE           (idx, 1)        = 0.00;
UNUSED_MEMSIZE            (idx, 1)        = 1172.17;

% Geometry parameters:

TOT_CELLS                 (idx, 1)        = 63 ;
UNION_CELLS               (idx, 1)        = 0 ;

% Neutron energy grid:

NEUTRON_ERG_TOL           (idx, 1)        =  0.00000E+00 ;
NEUTRON_ERG_NE            (idx, 1)        = 1021891 ;
NEUTRON_EMIN              (idx, 1)        =  1.00000E-11 ;
NEUTRON_EMAX              (idx, 1)        =  2.00000E+01 ;


% Unresolved resonance probability table sampling:

URES_DILU_CUT             (idx, 1)        =  1.00000E-09 ;
URES_EMIN                 (idx, 1)        =  1.00000E-06 ;
URES_EMAX                 (idx, 1)        =  9.81270E-01 ;
URES_AVAIL                (idx, 1)        = 202 ;
URES_USED                 (idx, 1)        = 164 ;

% Nuclides and reaction channels:

TOT_NUCLIDES              (idx, 1)        = 269 ;
TOT_TRANSPORT_NUCLIDES    (idx, 1)        = 269 ;
TOT_DOSIMETRY_NUCLIDES    (idx, 1)        = 0 ;
TOT_DECAY_NUCLIDES        (idx, 1)        = 0 ;
TOT_PHOTON_NUCLIDES       (idx, 1)        = 0 ;
TOT_REA_CHANNELS          (idx, 1)        = 7521 ;
TOT_TRANSMU_REA           (idx, 1)        = 0 ;

% Physics options:

USE_DELNU                 (idx, 1)        = 1 ;
USE_URES                  (idx, 1)        = 1 ;
USE_DBRC                  (idx, 1)        = 0 ;
IMPL_CAPT                 (idx, 1)        = 0 ;
IMPL_NXN                  (idx, 1)        = 1 ;
IMPL_FISS                 (idx, 1)        = 0 ;
DOPPLER_PREPROCESSOR      (idx, 1)        = 1 ;
ETTM_MODE                 (idx, 1)        = 0 ;
SAMPLE_FISS               (idx, 1)        = 1 ;
SAMPLE_CAPT               (idx, 1)        = 1 ;
SAMPLE_SCATT              (idx, 1)        = 1 ;

% Radioactivity data:

TOT_ACTIVITY              (idx, 1)        =  0.00000E+00 ;
TOT_DECAY_HEAT            (idx, 1)        =  0.00000E+00 ;
TOT_SF_RATE               (idx, 1)        =  0.00000E+00 ;
ACTINIDE_ACTIVITY         (idx, 1)        =  0.00000E+00 ;
ACTINIDE_DECAY_HEAT       (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_ACTIVITY  (idx, 1)        =  0.00000E+00 ;
FISSION_PRODUCT_DECAY_HEAT(idx, 1)        =  0.00000E+00 ;
INHALATION_TOXICITY       (idx, 1)        =  0.00000E+00 ;
INGESTION_TOXICITY        (idx, 1)        =  0.00000E+00 ;
SR90_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
TE132_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
I131_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
I132_ACTIVITY             (idx, 1)        =  0.00000E+00 ;
CS134_ACTIVITY            (idx, 1)        =  0.00000E+00 ;
CS137_ACTIVITY            (idx, 1)        =  0.00000E+00 ;

% Normaliation coefficient:

NORM_COEF                 (idx, [1:   4]) = [  4.95754E-06 8.4E-05  0.00000E+00 0.0E+00 ];

% Analog reaction rate estimators:

CONVERSION_RATIO          (idx, [1:   2]) = [  2.67510E-01 0.00045 ];
U235_FISS_FRAC            (idx, [1:   2]) = [  9.16315E-01 6.7E-05 ];
U238_FISS_FRAC            (idx, [1:   2]) = [  2.18385E-03 0.00475 ];
PU239_FISS_FRAC           (idx, [1:   2]) = [  8.05607E-02 0.00075 ];

% Normalized total reaction rates (neutrons):

TOT_POWER                 (idx, [1:   2]) = [  1.50877E-11 0.00011 ];
TOT_POWDENS               (idx, [1:   2]) = [  4.65473E-13 0.00011 ];
TOT_GENRATE               (idx, [1:   2]) = [  1.14982E+00 0.00011 ];
TOT_FISSRATE              (idx, [1:   2]) = [  4.65057E-01 0.00011 ];
TOT_CAPTRATE              (idx, [1:   2]) = [  4.74957E-01 8.7E-05 ];
TOT_ABSRATE               (idx, [1:   2]) = [  9.40014E-01 4.4E-05 ];
TOT_SRCRATE               (idx, [1:   2]) = [  9.91508E-01 8.4E-05 ];
TOT_FLUX                  (idx, [1:   2]) = [  4.63521E+02 0.00014 ];
TOT_LEAKRATE              (idx, [1:   2]) = [  5.99860E-02 0.00069 ];
ALBEDO_LEAKRATE           (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_LOSSRATE              (idx, [1:   2]) = [  1.00000E+00 0.0E+00 ];
TOT_CUTRATE               (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
TOT_RR                    (idx, [1:   2]) = [  1.89152E+02 0.00018 ];
INI_FMASS                 (idx, 1)        =  3.24137E-05 ;
TOT_FMASS                 (idx, 1)        =  3.24137E-05 ;

% Xe-135 entropy:

XE135_ENTROPY             (idx, 1)        =  0.00000E+00 ;

% Criticality eigenvalues:

ANA_KEFF                  (idx, [1:   6]) = [  1.15955E+00 0.00018  1.15245E+00 0.00017  7.15801E-03 0.00287 ];
IMP_KEFF                  (idx, [1:   2]) = [  1.15968E+00 0.00011 ];
COL_KEFF                  (idx, [1:   2]) = [  1.15967E+00 0.00015 ];
ABS_KEFF                  (idx, [1:   2]) = [  1.15968E+00 0.00011 ];
ABS_KINF                  (idx, [1:   2]) = [  1.23436E+00 8.8E-05 ];
GEOM_ALBEDO               (idx, [1:   6]) = [  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00  1.00000E+00 0.0E+00 ];

% Forward-weighted time constants:

FWD_IMP_GEN_TIME          (idx, [1:   2]) = [  3.90399E-04 0.00034 ];
FWD_IMP_LIFETIME          (idx, [1:   2]) = [  4.52737E-04 0.00029 ];
FWD_ANA_BETA_ZERO         (idx, [1:  14]) = [  5.36395E-03 0.00224  1.71258E-04 0.01092  9.14533E-04 0.00555  8.63050E-04 0.00527  2.45402E-03 0.00318  7.09281E-04 0.00570  2.51812E-04 0.00935 ];
FWD_ANA_LAMBDA            (idx, [1:  14]) = [  7.54271E-01 0.00487  1.24905E-02 1.7E-05  3.17147E-02 6.3E-05  1.09323E-01 3.1E-05  3.17155E-01 1.9E-05  1.35260E+00 8.6E-05  8.66628E+00 0.00038 ];

% Beta-eff using Meulekamp's method:

ADJ_MEULEKAMP_BETA_EFF    (idx, [1:  14]) = [  6.16120E-03 0.00291  1.96748E-04 0.01487  1.05034E-03 0.00685  9.92669E-04 0.00705  2.81946E-03 0.00411  8.13896E-04 0.00760  2.88091E-04 0.01272 ];
ADJ_MEULEKAMP_LAMBDA      (idx, [1:  14]) = [  7.52303E-01 0.00657  1.24907E-02 2.6E-05  3.17161E-02 8.2E-05  1.09327E-01 4.1E-05  3.17151E-01 2.5E-05  1.35250E+00 0.00012  8.66470E+00 0.00044 ];

% Adjoint weighted time constants using Nauchi's method:

ADJ_NAUCHI_GEN_TIME       (idx, [1:   6]) = [  3.37778E-04 0.00049  3.37887E-04 0.00049  3.20393E-04 0.00662 ];
ADJ_NAUCHI_LIFETIME       (idx, [1:   6]) = [  3.91667E-04 0.00046  3.91793E-04 0.00047  3.71499E-04 0.00660 ];
ADJ_NAUCHI_BETA_EFF       (idx, [1:  14]) = [  6.17319E-03 0.00292  1.96252E-04 0.01691  1.05521E-03 0.00707  9.98429E-04 0.00714  2.81740E-03 0.00447  8.19707E-04 0.00804  2.86196E-04 0.01323 ];
ADJ_NAUCHI_LAMBDA         (idx, [1:  14]) = [  7.49745E-01 0.00692  1.24907E-02 3.0E-05  3.17172E-02 8.8E-05  1.09330E-01 4.9E-05  3.17151E-01 2.7E-05  1.35269E+00 0.00011  8.66178E+00 0.00051 ];

% Adjoint weighted time constants using IFP:

ADJ_IFP_GEN_TIME          (idx, [1:   6]) = [  3.23147E-04 0.00132  3.23240E-04 0.00132  3.07886E-04 0.01602 ];
ADJ_IFP_LIFETIME          (idx, [1:   6]) = [  3.74703E-04 0.00131  3.74810E-04 0.00131  3.56987E-04 0.01599 ];
ADJ_IFP_IMP_BETA_EFF      (idx, [1:  14]) = [  6.17281E-03 0.00940  1.84452E-04 0.05071  1.06262E-03 0.02163  1.03312E-03 0.02200  2.80428E-03 0.01448  8.12695E-04 0.02652  2.75635E-04 0.04421 ];
ADJ_IFP_IMP_LAMBDA        (idx, [1:  14]) = [  7.32215E-01 0.02321  1.24903E-02 7.2E-06  3.17169E-02 0.00032  1.09321E-01 0.00017  3.17164E-01 9.0E-05  1.35223E+00 0.00052  8.65941E+00 0.00288 ];
ADJ_IFP_ANA_BETA_EFF      (idx, [1:  14]) = [  6.18524E-03 0.00908  1.86709E-04 0.05012  1.06618E-03 0.02133  1.03343E-03 0.02141  2.80885E-03 0.01378  8.14470E-04 0.02619  2.75603E-04 0.04267 ];
ADJ_IFP_ANA_LAMBDA        (idx, [1:  14]) = [  7.30925E-01 0.02249  1.24903E-02 6.8E-06  3.17172E-02 0.00032  1.09315E-01 0.00016  3.17165E-01 8.6E-05  1.35230E+00 0.00049  8.65661E+00 0.00278 ];
ADJ_IFP_ROSSI_ALPHA       (idx, [1:   2]) = [ -1.91029E+01 0.00947 ];

% Adjoint weighted time constants using perturbation technique:

ADJ_PERT_GEN_TIME         (idx, [1:   2]) = [  3.31270E-04 0.00026 ];
ADJ_PERT_LIFETIME         (idx, [1:   2]) = [  3.84121E-04 0.00019 ];
ADJ_PERT_BETA_EFF         (idx, [1:   2]) = [  6.21446E-03 0.00159 ];
ADJ_PERT_ROSSI_ALPHA      (idx, [1:   2]) = [ -1.87597E+01 0.00161 ];

% Inverse neutron speed :

ANA_INV_SPD               (idx, [1:   2]) = [  9.68426E-07 0.00016 ];

% Analog slowing-down and thermal neutron lifetime (total/prompt/delayed):

ANA_SLOW_TIME             (idx, [1:   6]) = [  3.32164E-05 6.9E-05  3.32141E-05 6.9E-05  3.35948E-05 0.00086 ];
ANA_THERM_TIME            (idx, [1:   6]) = [  6.30796E-04 0.00031  6.31025E-04 0.00031  5.92853E-04 0.00382 ];
ANA_THERM_FRAC            (idx, [1:   6]) = [  6.77809E-01 0.00010  6.77373E-01 0.00011  7.59420E-01 0.00348 ];
ANA_DELAYED_EMTIME        (idx, [1:   2]) = [  1.09190E+01 0.00428 ];

% Parameters for group constant generation

GC_UNIVERSE_NAME          (idx, [1:  1])  = '0' ;
GC_NE                     (idx, 1)        = 2 ;
GC_BOUNDS                 (idx, [1:   3]) = [  2.00000E+01  6.25000E-07  1.00000E-11 ];

% Few-group cross sections:

FLUX                      (idx, [1:   6]) = [  4.63521E+02 0.00014  2.47474E+02 8.0E-05  2.16047E+02 0.00030 ];
LEAK                      (idx, [1:   6]) = [  5.99860E-02 0.00069  4.81328E-03 0.00270  5.51727E-02 0.00070 ];
TOTXS                     (idx, [1:   6]) = [  4.08075E-01 4.4E-05  3.56298E-01 1.9E-05  4.67383E-01 4.0E-05 ];
FISSXS                    (idx, [1:   6]) = [  1.00332E-03 0.00020  3.59349E-04 0.00032  1.74098E-03 0.00036 ];
CAPTXS                    (idx, [1:   6]) = [  1.02468E-03 0.00016  9.70793E-04 0.00024  1.08640E-03 0.00024 ];
ABSXS                     (idx, [1:   6]) = [  2.02799E-03 0.00016  1.33014E-03 0.00021  2.82739E-03 0.00031 ];
RABSXS                    (idx, [1:   6]) = [  2.00965E-03 0.00016  1.29578E-03 0.00022  2.82739E-03 0.00031 ];
ELAXS                     (idx, [1:   6]) = [  4.03775E-01 4.6E-05  3.50713E-01 1.9E-05  4.64556E-01 4.2E-05 ];
INELAXS                   (idx, [1:   6]) = [  2.27179E-03 0.00018  4.25508E-03 9.3E-05  2.09651E-17 6.0E-05 ];
SCATTXS                   (idx, [1:   6]) = [  4.06047E-01 4.5E-05  3.54968E-01 1.9E-05  4.64556E-01 4.2E-05 ];
SCATTPRODXS               (idx, [1:   6]) = [  4.06065E-01 4.5E-05  3.55003E-01 1.9E-05  4.64556E-01 4.2E-05 ];
REMXS                     (idx, [1:   6]) = [  2.00968E-03 0.00017  7.37363E-03 0.00016  6.70666E-03 0.00021 ];
NUBAR                     (idx, [1:   6]) = [  2.47243E+00 1.1E-05  2.45197E+00 1.7E-05  2.47727E+00 1.3E-05 ];
NSF                       (idx, [1:   6]) = [  2.48064E-03 0.00021  8.81114E-04 0.00032  4.31288E-03 0.00036 ];
RECIPVEL                  (idx, [1:   6]) = [  9.68426E-07 0.00016  1.17489E-07 7.5E-05  1.94315E-06 2.3E-05 ];
FISSE                     (idx, [1:   6]) = [  2.02492E+02 4.9E-07  2.02209E+02 5.7E-07  2.02558E+02 5.5E-07 ];

% Fission product poison data:

I135PRODXS                (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
XE135PRODXS               (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
PM149PRODXS               (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
SM149PRODXS               (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
I135ABSXS                 (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
XE135ABSXS                (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
PM149ABSXS                (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
SM149ABSXS                (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Fission spectra:

CHI                       (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
CHIP                      (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
CHID                      (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Group-transfer probabilities and cross sections:

GTRANSFP                  (idx, [1:   8]) = [  9.82878E-01 3.4E-06  8.35025E-03 0.00023  1.71223E-02 0.00019  9.91650E-01 1.9E-06 ];
GTRANSFXS                 (idx, [1:   8]) = [  3.48890E-01 1.8E-05  3.87916E-03 0.00022  6.07789E-03 0.00020  4.60677E-01 4.3E-05 ];

% Group-production probabilities and cross sections:

GPRODP                    (idx, [1:   8]) = [  9.82974E-01 3.4E-06  8.35025E-03 0.00023  1.71223E-02 0.00019  9.91650E-01 1.9E-06 ];
GPRODXS                   (idx, [1:   8]) = [  3.48925E-01 1.8E-05  3.87916E-03 0.00022  6.07789E-03 0.00020  4.60677E-01 4.3E-05 ];

% PN scattering cross sections:

SCATT0                    (idx, [1:   6]) = [  4.06047E-01 4.5E-05  3.54968E-01 1.9E-05  4.64556E-01 4.2E-05 ];
SCATT1                    (idx, [1:   6]) = [  1.97937E-02 0.00014  2.24664E-02 0.00016  1.67322E-02 0.00026 ];
SCATT2                    (idx, [1:   6]) = [  1.17576E-05 0.18308  2.54722E-03 0.00105 -2.89252E-03 0.00114 ];
SCATT3                    (idx, [1:   6]) = [ -1.07209E-03 0.00154  4.93853E-04 0.00461 -2.86581E-03 0.00089 ];
SCATT4                    (idx, [1:   6]) = [ -2.37076E-03 0.00062 -1.85787E-04 0.01035 -4.87357E-03 0.00047 ];
SCATT5                    (idx, [1:   6]) = [ -1.16607E-03 0.00129  1.49679E-04 0.01229 -2.67321E-03 0.00075 ];

% P1 diffusion parameters:

P1_TRANSPXS               (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
P1_DIFFCOEF               (idx, [1:   6]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
P1_MUBAR                  (idx, [1:   6]) = [  4.87472E-02 0.00015  6.32912E-02 0.00016  3.60176E-02 0.00026 ];

% Micro- and macro-group structures:

MICRO_NG                  (idx, 1)        = 70 ;
MICRO_E                   (idx, [1:  71]) = [  1.00000E+01  6.06550E+00  3.67900E+00  2.23100E+00  1.35300E+00  8.21000E-01  5.00000E-01  3.02500E-01  1.83000E-01  1.11000E-01  6.74300E-02  4.08500E-02  2.47800E-02  1.50300E-02  9.11800E-03  5.53000E-03  3.51910E-03  2.23945E-03  1.42510E-03  9.06898E-04  3.67262E-04  1.48728E-04  7.55014E-05  4.80520E-05  2.77000E-05  1.59680E-05  9.87700E-06  4.00000E-06  3.30000E-06  2.60000E-06  2.10000E-06  1.85500E-06  1.50000E-06  1.30000E-06  1.15000E-06  1.12300E-06  1.09700E-06  1.07100E-06  1.04500E-06  1.02000E-06  9.96000E-07  9.72000E-07  9.50000E-07  9.10000E-07  8.50000E-07  7.80000E-07  6.25000E-07  5.00000E-07  4.00000E-07  3.50000E-07  3.20000E-07  3.00000E-07  2.80000E-07  2.50000E-07  2.20000E-07  1.80000E-07  1.40000E-07  1.00000E-07  8.00000E-08  6.70000E-08  5.80000E-08  5.00000E-08  4.20000E-08  3.50000E-08  3.00000E-08  2.50000E-08  2.00000E-08  1.50000E-08  1.00000E-08  5.00000E-09  1.00000E-11 ];

MACRO_NG                  (idx, 1)        = 2 ;
MACRO_E                   (idx, [1:   3]) = [  1.00000E+37  6.25000E-07  0.00000E+00 ];

% Integral parameters:

INF_KINF                  (idx, [1:   2]) = [  1.23438E+00 0.00019 ];

% Flux spectrum in infinite geometry:

INF_FLX                   (idx, [1:   4]) = [  2.47453E+02 6.0E-05  2.16048E+02 0.00029 ];

% Reaction cross sections:

INF_TOT                   (idx, [1:   4]) = [  3.56318E-01 2.8E-05  4.67384E-01 3.5E-05 ];
INF_CAPT                  (idx, [1:   4]) = [  9.70240E-04 0.00026  1.08639E-03 0.00022 ];
INF_ABS                   (idx, [1:   4]) = [  1.32960E-03 0.00025  2.82734E-03 0.00028 ];
INF_FISS                  (idx, [1:   4]) = [  3.59361E-04 0.00030  1.74095E-03 0.00032 ];
INF_NSF                   (idx, [1:   4]) = [  8.80724E-04 0.00045  4.31294E-03 0.00037 ];
INF_NUBAR                 (idx, [1:   4]) = [  2.45081E+00 0.00046  2.47735E+00 0.00018 ];
INF_KAPPA                 (idx, [1:   4]) = [  2.02209E+02 3.1E-07  2.02558E+02 6.1E-07 ];
INF_INVV                  (idx, [1:   4]) = [  1.17499E-07 6.9E-05  1.94315E-06 2.0E-05 ];

% Total scattering cross sections:

INF_SCATT0                (idx, [1:   4]) = [  3.54988E-01 2.8E-05  4.64557E-01 3.6E-05 ];
INF_SCATT1                (idx, [1:   4]) = [  2.24638E-02 0.00012  1.67322E-02 0.00021 ];
INF_SCATT2                (idx, [1:   4]) = [  2.54419E-03 0.00058 -2.89254E-03 0.00105 ];
INF_SCATT3                (idx, [1:   4]) = [  4.91618E-04 0.00344 -2.86583E-03 0.00087 ];
INF_SCATT4                (idx, [1:   4]) = [ -1.87177E-04 0.00710 -4.87358E-03 0.00039 ];
INF_SCATT5                (idx, [1:   4]) = [  1.49045E-04 0.01337 -2.67320E-03 0.00092 ];
INF_SCATT6                (idx, [1:   4]) = [ -3.96811E-04 0.00345 -5.97080E-03 0.00026 ];
INF_SCATT7                (idx, [1:   4]) = [  1.98094E-04 0.00910 -7.20077E-04 0.00227 ];

% Total scattering production cross sections:

INF_SCATTP0               (idx, [1:   4]) = [  3.55022E-01 2.8E-05  4.64557E-01 3.6E-05 ];
INF_SCATTP1               (idx, [1:   4]) = [  2.24728E-02 0.00012  1.67322E-02 0.00021 ];
INF_SCATTP2               (idx, [1:   4]) = [  2.54586E-03 0.00058 -2.89254E-03 0.00105 ];
INF_SCATTP3               (idx, [1:   4]) = [  4.91900E-04 0.00343 -2.86583E-03 0.00087 ];
INF_SCATTP4               (idx, [1:   4]) = [ -1.87154E-04 0.00714 -4.87358E-03 0.00039 ];
INF_SCATTP5               (idx, [1:   4]) = [  1.49022E-04 0.01334 -2.67320E-03 0.00092 ];
INF_SCATTP6               (idx, [1:   4]) = [ -3.96830E-04 0.00344 -5.97080E-03 0.00026 ];
INF_SCATTP7               (idx, [1:   4]) = [  1.98065E-04 0.00906 -7.20077E-04 0.00227 ];

% Diffusion parameters:

INF_TRANSPXS              (idx, [1:   4]) = [  3.14079E-01 3.6E-05  4.48840E-01 3.5E-05 ];
INF_DIFFCOEF              (idx, [1:   4]) = [  1.06130E+00 3.6E-05  7.42656E-01 3.5E-05 ];

% Reduced absoption and removal:

INF_RABSXS                (idx, [1:   4]) = [  1.29549E-03 0.00025  2.82734E-03 0.00028 ];
INF_REMXS                 (idx, [1:   4]) = [  7.40797E-03 0.00013  6.70660E-03 0.00020 ];

% Poison cross sections:

INF_I135_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_XE135_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM149_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_SM149_YIELD           (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_I135_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_XE135_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_PM149_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_SM149_MICRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_XE135_MACRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_SM149_MACRO_ABS       (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Fission spectra:

INF_CHIT                  (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_CHIP                  (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
INF_CHID                  (idx, [1:   4]) = [  1.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Scattering matrixes:

INF_S0                    (idx, [1:   8]) = [  3.48910E-01 2.6E-05  6.07840E-03 0.00018  3.87915E-03 0.00018  4.60677E-01 3.7E-05 ];
INF_S1                    (idx, [1:   8]) = [  2.36952E-02 0.00011 -1.23138E-03 0.00029 -5.09642E-04 0.00065  1.72418E-02 0.00021 ];
INF_S2                    (idx, [1:   8]) = [  2.81882E-03 0.00052 -2.74621E-04 0.00063 -2.37904E-04 0.00081 -2.65464E-03 0.00111 ];
INF_S3                    (idx, [1:   8]) = [  5.69417E-04 0.00280 -7.77992E-05 0.00377 -7.94442E-05 0.00243 -2.78639E-03 0.00091 ];
INF_S4                    (idx, [1:   8]) = [ -1.27082E-04 0.01094 -6.00951E-05 0.00350 -5.34392E-05 0.00367 -4.82014E-03 0.00041 ];
INF_S5                    (idx, [1:   8]) = [  1.55535E-04 0.01297 -6.48980E-06 0.03003 -1.08930E-05 0.01731 -2.66231E-03 0.00091 ];
INF_S6                    (idx, [1:   8]) = [ -3.56066E-04 0.00383 -4.07450E-05 0.00459 -3.72882E-05 0.00379 -5.93352E-03 0.00026 ];
INF_S7                    (idx, [1:   8]) = [  1.65760E-04 0.01065  3.23339E-05 0.00432  1.89630E-05 0.00731 -7.39040E-04 0.00213 ];

% Scattering production matrixes:

INF_SP0                   (idx, [1:   8]) = [  3.48944E-01 2.6E-05  6.07840E-03 0.00018  3.87915E-03 0.00018  4.60677E-01 3.7E-05 ];
INF_SP1                   (idx, [1:   8]) = [  2.37042E-02 0.00010 -1.23138E-03 0.00029 -5.09642E-04 0.00065  1.72418E-02 0.00021 ];
INF_SP2                   (idx, [1:   8]) = [  2.82049E-03 0.00052 -2.74621E-04 0.00063 -2.37904E-04 0.00081 -2.65464E-03 0.00111 ];
INF_SP3                   (idx, [1:   8]) = [  5.69699E-04 0.00280 -7.77992E-05 0.00377 -7.94442E-05 0.00243 -2.78639E-03 0.00091 ];
INF_SP4                   (idx, [1:   8]) = [ -1.27059E-04 0.01099 -6.00951E-05 0.00350 -5.34392E-05 0.00367 -4.82014E-03 0.00041 ];
INF_SP5                   (idx, [1:   8]) = [  1.55512E-04 0.01294 -6.48980E-06 0.03003 -1.08930E-05 0.01731 -2.66231E-03 0.00091 ];
INF_SP6                   (idx, [1:   8]) = [ -3.56085E-04 0.00382 -4.07450E-05 0.00459 -3.72882E-05 0.00379 -5.93352E-03 0.00026 ];
INF_SP7                   (idx, [1:   8]) = [  1.65731E-04 0.01059  3.23339E-05 0.00432  1.89630E-05 0.00731 -7.39040E-04 0.00213 ];

% Integral parameters:

B1_KINF                   (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
B1_KEFF                   (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
B1_B2                     (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];
B1_ERR                    (idx, [1:   2]) = [  0.00000E+00 0.0E+00 ];

% Critical spectrum in infinite geometry:

B1_FLX                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Reaction cross sections:

B1_TOT                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_CAPT                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_ABS                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_FISS                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_NSF                    (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_NUBAR                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_KAPPA                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_INVV                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Total scattering cross sections:

B1_SCATT0                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT1                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT2                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT3                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT4                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT5                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT6                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATT7                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Total scattering production cross sections:

B1_SCATTP0                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP1                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP2                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP3                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP4                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP5                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP6                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SCATTP7                (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Diffusion parameters:

B1_TRANSPXS               (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_DIFFCOEF               (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Reduced absoption and removal:

B1_RABSXS                 (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_REMXS                  (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Poison cross sections:

B1_I135_YIELD             (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_XE135_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM149_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SM149_YIELD            (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_I135_MICRO_ABS         (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_XE135_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_PM149_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SM149_MICRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_XE135_MACRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SM149_MACRO_ABS        (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Fission spectra:

B1_CHIT                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_CHIP                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_CHID                   (idx, [1:   4]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Scattering matrixes:

B1_S0                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S1                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S2                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S3                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S4                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S5                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S6                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_S7                     (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

% Scattering production matrixes:

B1_SP0                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP1                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP2                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP3                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP4                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP5                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP6                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];
B1_SP7                    (idx, [1:   8]) = [  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00  0.00000E+00 0.0E+00 ];

