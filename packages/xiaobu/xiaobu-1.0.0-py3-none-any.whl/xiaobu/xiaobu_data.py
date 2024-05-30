from sqlalchemy import create_engine, Column, Integer, String, and_, Date, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库连接
engine = create_engine('mysql+pymysql://root:XBJmysql126%40@192.168.1.22:3306/test_data?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
data_session = Session()


# 店铺
class TmPromotion(Base):
    __tablename__ = 'data_tm_link_promotion'

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, nullable=False)
    promotionId = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)
    charge = Column(Numeric(15, 2), nullable=False)
    alipayInshopAmt = Column(Numeric(15, 2), nullable=False)
    click = Column(Integer, nullable=False)
    adPv = Column(Integer, nullable=False)

    @staticmethod
    def upsert(data: list, date, shop_id):
        batchs = []
        for i in data:
            existing_data = data_session.query(TmPromotion).filter(
                and_(TmPromotion.date == date,
                     TmPromotion.shop_id == shop_id,
                     TmPromotion.promotionId == i['promotionId'])
            ).first()
            if existing_data:
                for key, value in i.items():
                    setattr(existing_data, key, value)
                batchs.append(existing_data)
            else:
                batchs.append(TmPromotion(date=date,
                                          shop_id=shop_id,
                                          promotionId=i['promotionId'],
                                          alipayInshopAmt=i['alipayInshopAmt'],
                                          charge=i['charge'],
                                          type=i['type'],
                                          click=i['click'],
                                          adPv=i['adPv']))
        data_session.bulk_save_objects(batchs)
        data_session.commit()


class TmCTB(Base):
    __tablename__ = 'data_tm_link_ctb'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    shop_id = Column(Integer, nullable=False)
    link_id = Column(String(20), nullable=False)

    sales = Column(Numeric(15, 2), nullable=False)
    refund = Column(Numeric(15, 2), nullable=False)
    replenish = Column(Numeric(15, 2), nullable=False)
    replenish_count = Column(Integer, nullable=False)

    @staticmethod
    def upsert(data: list, date, shop_id):
        batches = []
        for i in data:
            existing_data = data_session.query(TmCTB).filter(
                and_(TmCTB.date == date,
                     TmCTB.shop_id == shop_id,
                     TmCTB.link_id == i['link_id'])
            ).first()
            if existing_data:
                for key, value in i.items():
                    setattr(existing_data, key, value)
                batches.append(existing_data)
            else:
                batches.append(TmCTB(date=date,
                                    shop_id=shop_id,
                                    link_id=i['link_id'],
                                    sales=i['sales'],
                                    refund=i['refund'],
                                    replenish=i['replenish'],
                                    replenish_count=i['replenish_count']
                                    ))
        data_session.bulk_save_objects(batches)
        data_session.commit()


def create_table():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_table()
