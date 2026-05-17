from enum import StrEnum


class CuisineType(StrEnum):
    # Europe
    FRENCH = "french"
    ITALIAN = "italian"
    SPANISH = "spanish"
    PORTUGUESE = "portuguese"
    GREEK = "greek"
    TURKISH = "turkish"
    GERMAN = "german"
    BRITISH = "british"
    IRISH = "irish"
    BELGIAN = "belgian"
    DUTCH = "dutch"
    SWISS = "swiss"
    AUSTRIAN = "austrian"
    POLISH = "polish"
    HUNGARIAN = "hungarian"
    CZECH = "czech"
    SCANDINAVIAN = "scandinavian"
    SWEDISH = "swedish"
    NORWEGIAN = "norwegian"
    FINNISH = "finnish"
    DANISH = "danish"
    BALKAN = "balkan"
    RUSSIAN = "russian"
    UKRAINIAN = "ukrainian"

    # East Asia
    CHINESE = "chinese"
    JAPANESE = "japanese"
    KOREAN = "korean"
    TAIWANESE = "taiwanese"
    MONGOLIAN = "mongolian"

    # Southeast Asia
    THAI = "thai"
    VIETNAMESE = "vietnamese"
    INDONESIAN = "indonesian"
    MALAYSIAN = "malaysian"
    FILIPINO = "filipino"
    SINGAPOREAN = "singaporean"
    CAMBODIAN = "cambodian"
    LAOTIAN = "laotian"
    BURMESE = "burmese"

    # South Asia
    INDIAN = "indian"
    PAKISTANI = "pakistani"
    BANGLADESHI = "bangladeshi"
    SRI_LANKAN = "sri_lankan"
    NEPALESE = "nepalese"

    # Middle East & Central Asia
    LEBANESE = "lebanese"
    SYRIAN = "syrian"
    PERSIAN = "persian"
    ISRAELI = "israeli"
    ARABIAN = "arabian"
    AFGHAN = "afghan"
    UZBEK = "uzbek"

    # Africa
    MOROCCAN = "moroccan"
    ALGERIAN = "algerian"
    TUNISIAN = "tunisian"
    ETHIOPIAN = "ethiopian"
    SENEGALESE = "senegalese"
    SOUTH_AFRICAN = "south_african"
    NIGERIAN = "nigerian"

    # Americas
    AMERICAN = "american"
    CANADIAN = "canadian"
    MEXICAN = "mexican"
    TEX_MEX = "tex_mex"
    BRAZILIAN = "brazilian"
    ARGENTINIAN = "argentinian"
    PERUVIAN = "peruvian"
    COLOMBIAN = "colombian"
    CARIBBEAN = "caribbean"
    CUBAN = "cuban"
    JAMAICAN = "jamaican"

    # Oceania
    AUSTRALIAN = "australian"
    NEW_ZEALAND = "new_zealand"
    POLYNESIAN = "polynesian"

    # Regional / style-based
    MEDITERRANEAN = "mediterranean"
    LATIN_AMERICAN = "latin_american"
    CAJUN = "cajun"
    CREOLE = "creole"
    SOUL_FOOD = "soul_food"
    BBQ = "bbq"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    SEAFOOD = "seafood"
    STREET_FOOD = "street_food"
    FUSION = "fusion"

    # Other
    OTHER = "other"
