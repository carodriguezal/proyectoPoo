import sqlite3
from datetime import datetime

def dataBaseConnection():
    try:
        connection = sqlite3.connect('database.db')
        print('\nÉxito al conectar a la base de datos de servicios')
        return connection
    except sqlite3.Error as error:
        print(f'Error al conectar a la base de datos de servicios: {error}')

def closeDataBaseConnection(connection):
    connection.close()

def createServicesTable(connection):
    cursor = connection.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS services(
        serviceCode INTEGER,
        serviceName TEXT,
        origin TEXT,
        destination TEXT,
        sellingPrice INTEGER,
        departureTime INTEGER,
        maximumSeatingCapacity INTEGER,
        maximumWeightCapacity INTEGER,
        PRIMARY KEY(serviceCode))'''
    cursor.execute(query)
    cursor.close()
    connection.commit()

def createCustomersTable(connection):
    cursor = connection.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS customers(
        customerID INTEGER,
        customerName TEXT,
        customerLastName TEXT,
        customerAddress TEXT,
        phoneNumber INTEGER,
        emailAddress TEXT,
        PRIMARY KEY(customerID))'''
    cursor.execute(query)
    cursor.close()
    connection.commit()

class service:
    def __init__(self):
        self.serviceCode = None
        self.serviceName = None
        self.origin = None
        self.destination = None
        self.sellingPrice = None
        self.departureTime = None
        self.maximumSeatingCapacity = None
        self.maximumWeightCapacity = None

    def createService(self, connection):
        self.serviceCode = input('\nCódigo del servicio: ')
        self.serviceName = input('Nombre del servicio: ')
        self.origin = input('Ciudad de origen: ')
        self.destination = input('Ciudad de destino: ')
        self.sellingPrice = input('Precio de venta (COP): ')
        self.departureTime = input('Hora de salida (HH:MM:SS): ')
        self.departureTime = datetime.strptime(f'1971-01-01 {self.departureTime}','%Y-%m-%d %H:%M:%S')
        self.departureTime = int(datetime.timestamp(self.departureTime))
        self.maximumSeatingCapacity = input('Cantidad de puestos disponibles: ')
        self.maximumWeightCapacity = input('Cantidad de peso disponible (Kilogramos): ')
        service = (
            self.serviceCode,
            self.serviceName,
            self.origin,
            self.destination,
            self.sellingPrice,
            self.departureTime,
            self.maximumSeatingCapacity,
            self.maximumWeightCapacity
        )
        cursor = connection.cursor()
        query = 'INSERT INTO services VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(query,service)
        cursor.close()
        connection.commit()

    def updateService(self, connection):
        self.serviceName = input(f'Nuevo nombre (servicio #{self.serviceCode}): ')
        cursor = connection.cursor()
        query = f'UPDATE services SET serviceName = "{self.serviceName}" WHERE serviceCode = {self.serviceCode}'
        cursor.execute(query)
        cursor.close()
        connection.commit()

    def consultService(self, connection): # Podría estar fuera de la clase, pero se exige como método
        serviceCode = input('Código del servicio: ')
        cursor = connection.cursor()
        query = f'SELECT * FROM services where serviceCode = {serviceCode}'
        cursor.execute(query)
        row = cursor.fetchone()
        if not row:
            print(f'\nNo existe servicio con código {serviceCode}')
        else:
            serviceCode = row[0]
            serviceName = row[1]
            origin = row[2]
            destination = row[3]
            sellingPrice = row[4]
            departureTime = datetime.fromtimestamp(row[5]).strftime("%H:%M:%S")
            maximumSeatingCapacity = row[6]
            maximumWeightCapacity = row[7]
            print(f'''
Resultado de la consulta:

    Código del servicio: {serviceCode}
    Nombre del servicio: {serviceName}
    Ciudad de origen: {origin}
    Ciudad de destino: {destination}
    Precio de venta (COP): {sellingPrice}
    Hora de salida (HH:MM:SS): {departureTime}
    Cantidad de puestos disponibles: {maximumSeatingCapacity}
    Cantidad de peso disponible (Kilogramos): {maximumWeightCapacity}''')
        cursor.close()
        connection.commit()

class customer:
    def __init__(self):
        self.customerID = None
        self.customerName = None
        self.customerLastName = None
        self.customerAddress = None
        self.phoneNumber = None
        self.emailAddress = None

    def createCustomer(self, connection):
        self.customerID = input('Número de identificación del cliente: ')
        self.customerName = input('Nombre del cliente: ')
        self.customerLastName = input('Apellido del cliente: ')
        self.customerAddress = input('Direccion del cliente: ')
        self.phoneNumber = input('Teléfono del cliente:')
        self.emailAddress = input('Direccion de correo electrónico: ')
        customer = (
            self.customerID,
            self.customerName,
            self.customerLastName,
            self.customerAddress,
            self.phoneNumber,
            self.emailAddress
        )
        cursor = connection.cursor()
        query = 'INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)'
        cursor.execute(query,customer)
        cursor.close()
        connection.commit()

    def updateCustomer(self, connection):
        self.customerAddress = input(f'Nueva dirección (cliente ID-{self.customerID}): ')
        cursor = connection.cursor()
        query = f'UPDATE customers SET customerAddress = "{self.customerAddress}" WHERE customerID = {self.customerID}'
        cursor.execute(query)
        cursor.close()
        connection.commit()

    def consultCustomer(self, connection):
        customerID = input('Número de identificación del cliente: ')
        cursor = connection.cursor()
        query = f'SELECT * FROM customers where customerID = {customerID}'
        cursor.execute(query)
        row = cursor.fetchone()
        if not row:
            print(f'\nNo existe cliente con ID {customerID}')
        else:
            customerID = row[0]
            customerName = row[1]
            customerLastName = row[2]
            customerAddress = row[3]
            phoneNumber = row[4]
            emailAddress = row[5]
            print(f'''
Resultado de la consulta:

    Número de identificación del cliente: {customerID}
    Nombre del cliente: {customerName}
    Apellido del cliente: {customerLastName}
    Direccion del cliente: {customerAddress}
    Teléfono del cliente: {phoneNumber}
    Direccion de correo electrónico: {emailAddress}''')
        cursor.close()
        connection.commit()

class sale(service, customer):
    def __init__(self):
        service.__init__(self)
        customer.__init__(self)
        self.invoiceNumber = None
        self.quantitySold = None

    def addServiceToSale(self, connection):
        servicesForSale = []
        while True:
            serviceCode = input('Código del servicio a añadir a la venta: ')
            cursor = connection.cursor()
            query = f'SELECT * FROM services where serviceCode = {serviceCode}'
            cursor.execute(query)
            row = cursor.fetchone()
            if not row:
                print(f'\nNo existe servicio con código {serviceCode}')
            else:
                servicesForSale.append(row)
            addAnotherService = input('¿Añadir otro servicio? (S/N): ').strip().upper()
            if addAnotherService != 'S':
                break
        print('Servicios añadidos a la venta:')
        for service in servicesForSale:
            print(service)

def menu(connection, serviceInstance, customerInstance, saleInstance):
    mainMenuExit = False
    while not mainMenuExit:
        mainMenuOption = input('''
Cooperativa de Transportes La Nacional - Menú Principal
                        
    1. Menú de gestión de servicios
    2. Menú de gestión de clientes
    3. Menú de gestión de ventas
    4. Impresión de facturas
    5. Salir                 
                        
Seleccione una opción... >>> ''')
        if(mainMenuOption == '1'):
            servicesMenuExit = False
            while not servicesMenuExit:
                servicesMenuOption = input('''
Cooperativa de Transportes La Nacional - Menú de gestión de servicios
                                           
    1. Crear el servicio
    2. Actualizar el nombre del servicio
    3. Consultar un servicio
    4. Salir
                           
Seleccione una opción... >>> ''')
                if (servicesMenuOption == '1'):
                    serviceInstance.createService(connection)
                elif (servicesMenuOption == '2'):
                    if serviceInstance.serviceCode == None:
                        print('\nSe debe crear primero el servicio')
                    else:
                        serviceInstance.updateService(connection)
                elif (servicesMenuOption == '3'):
                    serviceInstance.consultService(connection)
                elif (servicesMenuOption == '4'):
                    servicesMenuExit = True
        elif(mainMenuOption=='2'):
            customersMenuExit = False
            while not customersMenuExit:
                customerMenuOption = input('''
Cooperativa de Transportes La Nacional - Menú de gestión de clientes
                                           
    1. Crear un cliente
    2. Actualizar la dirección del cliente
    3. Consultar un cliente
    4. Salir
                           
Seleccione una opción... >>> ''')
                if (customerMenuOption == '1'):
                    customerInstance.createCustomer(connection)
                elif (customerMenuOption == '2'):
                    if customerInstance.customerID == None:
                        print('\nSe debe crear primero el cliente')
                    else:
                        customerInstance.updateCustomer(connection)
                elif (customerMenuOption == '3'):
                    customerInstance.consultCustomer(connection)
                elif (customerMenuOption == '4'):
                    customersMenuExit = True
        elif(mainMenuOption=='3'):
            salesMenuExit = False
            while not salesMenuExit:
                salesMenuOption = input('''
Cooperativa de Transportes La Nacional - Menú de gestión de ventas

    1. Añadir Servicio a vender
    2. Quitar Servicio añadido
                                        
Seleccione una opción... >>> ''')
                if (salesMenuOption == '1'): #Deberia añadir unicamente un servicio o varios?
                    saleInstance.addServiceToSale(connection)
                elif(salesMenuOption == '2'):
                    salesMenuExit = True
        elif(mainMenuOption=='4'):
            mainMenuExit=True
        elif(mainMenuOption=='5'):
            mainMenuExit=True

def main():
    connection = dataBaseConnection()
    createServicesTable(connection)
    createCustomersTable(connection)
    serviceInstance = service()
    customerInstance = customer()
    saleInstance = sale()
    menu(connection,serviceInstance,customerInstance,saleInstance)
    closeDataBaseConnection(connection)

main()

# Base de datos en Servicios
# Utilizar Unix para almacenar horas
# Que formato debe tener el noFactura para que no se repitan o sean unicos
# Caracteristicas primera y segunda entrega