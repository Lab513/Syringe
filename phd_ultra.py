import serial

class SERIAL_COM():
    '''
    '''
    def __init__(self, port='COM5'):
        self.ser = serial.Serial(port = port,
                                 baudrate = 9600,
                                 timeout=0.5)

    def send_cmd(self, cmd, rep=1, prt=True):
        '''
        Send a command
        '''
        self.ser.write(f'{cmd} \r\n'.encode())
        self.ser.readline()
        for i in range(rep):
            answ = str(self.ser.readline(),"utf-8").strip()
            if prt:
                print(f'{answ}')

    def set_or_ask(self, cmd, arg=''):
        '''
        '''
        if arg != '?':
            self.send_cmd(f'{cmd} {arg}', prt=False)
        else :
            self.send_cmd(f'{cmd}')


class SYRINGE(SERIAL_COM):
    '''
    '''

    def __init__(self):
        SERIAL_COM.__init__(self)
        self.dic_rate = {'INF': ['irate', 'infuse'],
                         'WD': ['wrate', 'withdraw']}
        # volume L
        self.vu = {'m': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12}
        # flow L/t
        self.fu = {'m': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12}
        self.tu = {'h': 3600, 'm': 60, 's': 1}

    def set_params(self,
                   direction='INF',
                   diam=11.99,
                   syr_vol=500.0,
                   targ_vol=500.0,
                   targ_time=None,
                   vol_unit='ml',
                   flow_rate=50.0,
                   flow_rate_unit='m/h',
                   force=90):
        '''
        m, u, n, p/h, m, s
        Ex: m/m= milliliter/minute
        n/s= nanoliter/second
        diam in mm
        '''

        self.direction = direction
        self.diam = diam
        self.targ_vol = float(targ_vol)
        self.vol_unit = vol_unit
        self.flow_rate = flow_rate
        self.flow_rate_unit = flow_rate_unit
        self.diameter(diam)
        self.syringe_volume(syr_vol)
        self.target_volume(targ_vol)
        self.force(force)
        self.set_rate(direction)
        self.expected_time()

    def expected_time(self):
        '''
        Expected time from target volume, diameter
        and flow_rate
        '''
        fact_diam_square = 1e-6
        fact_vol = self.vu[self.vol_unit[0]]
        fru = self.flow_rate_unit.split('/')
        fact_flow = float(self.fu[fru[0]])/self.tu[fru[1]]
        fact = fact_vol/(fact_flow*60.0)
        # surf in m**2
        syr_surf = 3.14159*(self.diam/2)**2
        # expected time in minutes
        exp_time = round(self.targ_vol/(self.flow_rate)*fact,2)
        print(f'Expected time is {exp_time} min')

    def set_rate(self, direction):
        '''
        '''
        speed = f'{self.flow_rate} {self.flow_rate_unit}'
        cmd = f'{self.dic_rate[direction][0]} {speed} '
        print(f'{self.dic_rate[direction][1]} @ {speed}')
        self.send_cmd(cmd, prt=False)

    def diameter(self, diam=11.99, debug=[0]):
        '''
        ask or set the diameter
        '''
        if 0 in debug:
            print(f'syringe diameter set to {diam} mm')
        self.set_or_ask('diam', diam)

    def syringe_volume(self, vol=500, debug=[0]):
        '''
        ask or set the volume
        '''
        val_vol = f'{vol} {self.vol_unit}'
        cmd = f'svol {val_vol}'
        if 0 in debug:
            print(f'syringe volume set to {val_vol}')
        self.send_cmd(cmd, prt=False)

    def target_volume(self, targ_vol=100, debug=[0]):
        '''
        ask or set the target volume
        '''
        val_targ_vol = f'{targ_vol} {self.vol_unit}'
        cmd = f'tvol {val_targ_vol}'
        if 0 in debug:
            print(f'target volume set to {val_targ_vol}')
        self.send_cmd(cmd, prt=False)

    def force(self, force=90):
        '''
        ask or set the diameter
        '''
        self.set_or_ask('force', force)

    #-----------------

    def infuse(self):
        '''
        '''
        self.set_or_ask('irun')

    def withdraw(self):
        '''
        '''
        self.set_or_ask('wrun')

    def run(self):
        '''
        launch the syringe
        '''
        if self.direction == 'INF':
            print('Infusing')
            self.infuse()
        elif self.direction == 'WD':
            print('Withdrawing')
            self.withdraw()

    def stop(self):
        '''
        Stop the syringe
        '''
        self.send_cmd('STP', prt=False)
