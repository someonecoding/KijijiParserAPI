from parser_session import ParserSession



session = ParserSession()
url = 'https://www.kijiji.ca/anvil/api'

async def anvil_get_profile(id):
    r = session.post(
        url=url,
        payload=[
                    {
            "operationName": "GetProfile",
            "variables": {
                "userId": id
            },
            "query": '''
            query GetProfile($userId: Long) {
                  findProfile(id: $userId) {
                        ...CoreProfile
                        numberOfOrganicAds
                        responsiveness
                        replyRate
                        __typename
                    }
            }
                                          
            fragment CoreProfile on Profile {
                companyName
                displayName
                id
                isAdmarkt
                isReadIndicatorEnabled
                isSfidEnabled
                memberSince
                photoUrl
                profileName
                profileType
                __typename
            }
            '''
            }
        ]
    )

    return await r


async def anvil_get_profile_phone(adid, sellerid, vipurl, sellername):
    session = ParserSession()
    r = session.post(
        url=url,
        payload=[{
            "operationName": "GetDynamicPhoneNumber",
            "variables": {
                "adId": str(adid),
                "sellerId": str(sellerid),
                "vipUrl": vipurl,
                "listingType": "rent",
                "sellerName": sellername
            },
            "query": '''
            query GetDynamicPhoneNumber($sellerId: String!, $adId: String!, $userId: String, $vipUrl: String!, $listingType: String!, $sellerName: String!) {
                  getDynamicPhoneNumber(sellerId: $sellerId, adId: $adId, userId: $userId, vipUrl: $vipUrl, listingType: $listingType, sellerName: $sellerName) {
                        local
                        e164
                        __typename
            }}
            '''
        }
                ]
    )

    return await r




