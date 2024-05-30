import json

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, and_, DateTime
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:XBJmysql126%40@192.168.1.22:3306/test_center?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
center_session = Session()


# 店铺
class Shop(Base):
    __tablename__ = 'center_shop'

    id = Column(Integer, primary_key=True)
    erp_id = Column(Integer, nullable=False, unique=True)
    shop_name = Column(String(50), nullable=False, unique=True)
    platform = Column(String(10), nullable=False)
    is_open = Column(Integer, nullable=False, default=1)
    cookie = relationship('Cookie', backref='shop', uselist=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.shop_name)


# 店铺Cookie
class Cookie(Base):
    __tablename__ = 'center_cookie'

    id = Column(Integer, primary_key=True)
    value = Column(Text, nullable=False)
    is_syj = Column(Integer, nullable=False, default=0)
    update_time = Column(DateTime, nullable=True)
    shop_id = Column(Integer, ForeignKey('center_shop.id'))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.shop_id)


# 员工
class Employee(Base):
    __tablename__ = 'center_employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    account = Column(String(10), nullable=False)
    password = Column(String(300), nullable=False)
    status = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


def create_shop(shop_name, platform):
    to_create = Shop(shop_name=shop_name, platform=platform)
    center_session.add(to_create)
    center_session.commit()


def query_sname_by_sid(sid):
    return center_session.query(Shop.shop_name).filter(Shop.id == sid).first()[0]


def query_sid_by_sname(sname):
    return center_session.query(Shop.id).filter(Shop.shop_name == sname).first()[0]


def refresh_cookie(sid, cookie, is_syj=0):
    try:
        existing_cookie = center_session.query(Cookie).filter(
            and_(Cookie.shop_id == sid, Cookie.is_syj == is_syj)).one()
        existing_cookie.cookie = cookie
    except NoResultFound:
        new_cookie = Cookie(shop_id=sid, value=cookie, is_syj=is_syj)
        center_session.add(new_cookie)
    except Exception as e:
        center_session.rollback()
        raise e
    finally:
        center_session.commit()


def update_erp_shop_id(erp_id_path, sname):
    shop_id_name = json.load(open(erp_id_path, 'r', encoding='utf-8'))
    for shop in shop_id_name:
        if shop['name'] == sname:
            center_session.query(Shop).filter(Shop.shop_name == sname).update({'erp_id': shop['id']})
            center_session.commit()


def create_table():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_table()
