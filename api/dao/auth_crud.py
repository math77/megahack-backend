import uuid
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
import api.models as models
import api.schemas.employee_schemas.employee_schema as schemas
import api.schemas.auth_schemas.auth_schema as auth_schemas
import api.schemas.subscriber_schemas.subscriber_schema as subscriber_schemas

import bcrypt


class AuthDAO:

    """ TODO
        VERIFICAR SE A CONTA SENDO CRIADA VEM DO ECOMMERCE E EM CASO AFIRMATIVO VERIFICAR SE O EMAIL JA
        ESTÁ SENDO USADO NO ECOMMERCE ONDE A CONTA ESTA SENDO CRIADA E NÃO PERMITIR A CONTA.
    """
    @staticmethod
    def create_account(db: Session, account: auth_schemas.AuthCreateSchema):
        hashed_password = bcrypt.hashpw(account.password.encode('utf8'), bcrypt.gensalt()).decode('utf-8')

        db_auth = models.Auth(email=account.email, password=hashed_password, phone=account.phone)

        db.add(db_auth)
        db.commit()
        db.refresh(db_auth)
        
        return db_auth
    

    @staticmethod
    def verify_account_code(db: Session, phone: str, code: str):
        code_acc = db.query(models.AccountVerifyCode).filter(models.AccountVerifyCode.phone == phone).first()

        if code_acc is not None:

            if code_acc.code == code:
                return True
            return False
        return False
    

    @staticmethod
    def save_verify_account_code(db: Session, phone: str, code: str):
        db_acc_code = models.AccountVerifyCode(phone=phone, code=code)

        db.add(db_acc_code)
        db.commit()
        db.refresh(db_acc_code)

        return db_acc_code
    
    
    @staticmethod
    def create_subscriber(db: Session, subscriber: subscriber_schemas.SubscriberCreateSchema, id_auth: uuid):
        db_subscriber = models.ClientSubscriberTecnoinfo(full_name=subscriber.full_name,
                                                         first_name=subscriber.first_name,
                                                         last_name=subscriber.last_name,
                                                         id_auth=id_auth)


        db.add(db_subscriber)
        db.commit()
        db.refresh(db_subscriber)
        
        return db_subscriber
    
    
    @staticmethod
    def account_already_exist(db: Session, email: str):
        return db.query(models.Auth).filter(models.Auth.email == email).first()
    

    @staticmethod
    def create_ecommerce_account(db: Session, account: auth_schemas.AuthEcommerceCreateSchema):
        auth_r = AuthDAO.get_auth_by_email_2(db, account.email)

        db_auth = None

        # CONTA COM O EMAIL INFORMADO
        """
        if auth_r is not None:

            # ESSA CONTA JÁ FOI CADASTRADA NO ECOMMERCE ATUAL
            #account_in_ecommerce_ind = db.query(models.IndividualClient).filter(and_(models.IndividualClient.id_auth == auth_r.id, models.IndividualClient.id_company == uuid.UUID(account.id_ecommerce))).first()
            #account_in_ecommerce_corp = db.query(models.CorporateClient).filter(and_(models.CorporateClient.id_auth == auth_r.id, models.CorporateClient.id_company == uuid.UUID(account.id_ecommerce))).first()

            # JÁ FOI CADASTRADA NESTE ECOMMERCE
           
            if account_in_ecommerce_ind is not None or account_in_ecommerce_corp is not None:
                print("JA EXISTE")
        """

        hashed_password = bcrypt.hashpw(account.password.encode('utf8'), bcrypt.gensalt()).decode('utf-8')

        db_auth = models.Auth(email=account.email, password=hashed_password)

        db.add(db_auth)
        db.commit()
        db.refresh(db_auth)
        
        return db_auth
    
    @staticmethod
    def create_account_individual_client(db: Session, individual_client: auth_schemas.RegisterIndividualClientEcommerceCreateSchema, id_auth: uuid):
        db_individual_client = models.IndividualClient(first_name=individual_client.first_name,
                                                       last_name=individual_client.last_name,
                                                       cpf=individual_client.cpf,
                                                       id_auth=id_auth,
                                                       phone1=individual_client.cell_phone,
                                                       phone2=individual_client.phone_landline,
                                                       birth_date=individual_client.birth_date,
                                                       gender=individual_client.gender,
                                                       ecommerce_enabled=True,
                                                       id_company=uuid.UUID(individual_client.id_ecommerce))


        db.add(db_individual_client)
        db.commit()
        db.refresh(db_individual_client)

        return db_individual_client
    

    @staticmethod
    def create_account_corporate_client(db: Session, corporate_client: auth_schemas.RegisterCorporateClientEcommerceCreateSchema, id_auth: uuid):
        db_corporate_client = models.CorporateClient(fantasy_name=corporate_client.fantasy_name,
                                                     commercial_name=corporate_client.commercial_name,
                                                     cnpj=corporate_client.cnpj,
                                                     id_auth=id_auth,
                                                     phone1=corporate_client.cell_phone,
                                                     phone2=corporate_client.phone_landline,
                                                     id_sector=uuid.UUID(corporate_client.sector),
                                                     country_registration=corporate_client.country_registration,
                                                     ecommerce_enabled=True,
                                                     id_company=uuid.UUID(corporate_client.id_ecommerce))


        db.add(db_corporate_client)
        db.commit()
        db.refresh(db_corporate_client)

        return db_corporate_client

    
    @staticmethod
    def get_auth_by_email_2(db: Session, email: str):
        return db.query(models.Auth).filter(models.Auth.email == email).first()
    
    
    @staticmethod
    def get_individual_client_info(db: Session, id_auth: uuid):
        return db.query(models.IndividualClient).filter(and_(models.IndividualClient.id_auth == id_auth, models.IndividualClient.delivery_enabled==True)).first()

    
    @staticmethod
    def is_employee(db: Session, id_auth: uuid):
        return db.query(models.Employee).filter(models.Employee.id_auth == id_auth).first()
    

    @staticmethod
    def is_client_subscriber(db: Session, id_auth: uuid):
        return db.query(models.ClientSubscriberTecnoinfo).filter(models.ClientSubscriberTecnoinfo.id_auth == id_auth).first()
    
    @staticmethod
    def get_subscriber_head_office(db: Session, id_subscriber: uuid):
        return db.query(models.Company).filter(and_(models.Company.id_client_subscriber_tecnoinfo == id_subscriber, models.Company.is_head_office == True)).first()


    @staticmethod
    def get_client_ecommerce(db: Session, id_auth: uuid, id_ecommerce: str):
        
        individual_client = db.query(models.IndividualClient).filter(models.IndividualClient.id_auth == id_auth).first()
        corporate_client = db.query(models.CorporateClient).filter(models.CorporateClient.id_auth == id_auth).first()

        account_in_ecommerce = None

        if individual_client is not None:
            account_in_ecommerce = db.query(models.IndividualClient).filter(and_(models.IndividualClient.id_auth == id_auth, models.IndividualClient.ecommerce_enabled == True)).first()
        
        elif corporate_client is not None:
            account_in_ecommerce = db.query(models.CorporateClient).filter(and_(models.CorporateClient.id_auth == id_auth, models.CorporateClient.ecommerce_enabled == True)).first()
        
        else:
            #meter um log depois
            pass
        
        return account_in_ecommerce


    @staticmethod
    def get_employee_info(db: Session, id_auth: uuid):
        return db.query(models.Employee).filter(models.Employee.id_auth == id_auth).first()


    @staticmethod
    def check_auth_password(db: Session, account: auth_schemas.AuthenticateSchema):
        print("EMAILLL")
        print(account.email)
        print(account.password)
        db_account = AuthDAO.get_auth_by_email_2(db, email=account.email)
        print(db_account)
        print(db_account.id)
        print(db_account.password)
        return bcrypt.checkpw(account.password.encode('utf8'), db_account.password.encode('utf8'))


    @staticmethod
    def set_new_password(db: Session, password: str, id_user: str):
        auth = db.query(models.Auth).filter(models.Auth.id == uuid.UUID(id_user)).first()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        auth.password = hashed_password
        db.commit()
        return True
    
    @staticmethod
    def check_user_profile(db: Session, id_auth: uuid):
        user_client = db.query(models.UserClient).filter(models.UserClient.id_auth == id_auth).first()
        employee = db.query(models.Employee).filter(models.Employee.id_auth == id_auth).first()

        return user_client if user_client is not None else employee
