from fastapi import APIRouter, Depends, HTTPException, status
from api.logic import ads
from api.models.ads import AdDetails
from collections import defaultdict
from datetime import datetime



router = APIRouter(prefix='/ads', tags=['ads'])
logic = ads.AdsLogic()

@router.get('')
async def get_ads(
    min_price: int = None,
    max_price: int = None,
    min_date = None,
    max_date = None,
    ad_details: AdDetails = Depends()
    ):

    query = {'$and': [{}]}
    
    if min_price is not None:
        query['$and'].append(
            {'price': {'$gte': min_price}}
        )
    if max_price is not None:
        query['$and'].append(
            {'price': {'$lte': max_price}}
        )
    if min_date is not None:
        query['$and'].append(
            {'posted': {'$gte': datetime.strptime(min_date, '%Y-%m-%dT%H:%M:%S.%f%z')}}
        )
    if max_date is not None:
        query['$and'].append(
            {'posted': {'$lte': datetime.strptime(max_date, '%Y-%m-%dT%H:%M:%S.%f%z')}}
        )
    if ad_details.hydro is not None:
        query['$and'].append(
            {'hydro': {'$eq': ad_details.hydro}}
        )
    if ad_details.heat is not None:
        query['$and'].append(
            {'heat': {'$eq': ad_details.heat}}
        )
    if ad_details.water is not None:
        query['$and'].append(
            {'water': {'$eq': ad_details.water}}
        )
    if ad_details.internet is not None:
        query['$and'].append(
            {'internet': {'$eq': ad_details.internet}}
        )
    if ad_details.cable is not None:
        query['$and'].append(
            {'cable': {'$eq': ad_details.cable}}
        )
    if ad_details.parking is not None:
        query['$and'].append(
            {'parking': {'$eq': ad_details.parking}}
        )
    if ad_details.agreement is not None:
        query['$and'].append(
            {'agreement': {'$eq': ad_details.agreement}}
        )
    if ad_details.pets is not None:
        query['$and'].append(
            {'pets': {'$eq': ad_details.pets}}
        )
    if ad_details.min_size is not None:
        query['$and'].append(
            {'size': {'$gte': ad_details.min_size}}
        )
    if ad_details.max_size is not None:
        query['$and'].append(
            {'size': {'$lte': ad_details.max_size}}
        )
    if ad_details.furnished is not None:
        query['$and'].append(
            {'furnished': {'$eq': ad_details.furnished}}
        )
    if ad_details.laundry_iu is not None:
        query['$and'].append(
            {'laundry_iu': {'$eq': ad_details.laundry_iu}}
        )
    if ad_details.laundry_ib is not None:
        query['$and'].append(
            {'laundry_ib': {'$eq': ad_details.laundry_ib}}
        )
    if ad_details.dishwasher is not None:
        query['$and'].append(
            {'dishwasher': {'$eq': ad_details.dishwasher}}
        )
    if ad_details.fridge is not None:
        query['$and'].append(
            {'fridge': {'$eq': ad_details.fridge}}
        )
    if ad_details.conditioning is not None:
        query['$and'].append(
            {'conditioning': {'$eq': ad_details.conditioning}}
        )
    if ad_details.yard is not None:
        query['$and'].append(
            {'yard': {'$eq': ad_details.yard}}
        )
    if ad_details.balcony is not None:
        query['$and'].append(
            {'balcony': {'$eq': ad_details.balcony}}
        )
    if ad_details.smoking is not None:
        query['$and'].append(
            {'smoking': {'$eq': ad_details.smoking}}
        )

    return await logic.find_by_query(query)