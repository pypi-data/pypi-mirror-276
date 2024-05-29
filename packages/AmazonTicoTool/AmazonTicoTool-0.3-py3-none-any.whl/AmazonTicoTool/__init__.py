import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import browser_cookie3
from time import sleep


def mid_way_Authentication():
        
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--acceptInsecureCerts")
        options.add_argument("--disable-notifications")
        prefs = {
        "safebrowsing.enabled": True,
        "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)
        cj = browser_cookie3.firefox()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        driver.get('https://midway-auth.amazon.com')
        cj = browser_cookie3.firefox()
        for FX_cookie in cj:
                try:
                        if 'midway-auth.amazon.com' in str(FX_cookie.domain):
                                cookie_dict = {'domain': FX_cookie.domain, 'name': FX_cookie.name, 'value': FX_cookie.value}
                                driver.add_cookie(cookie_dict)
                except Exception as e:
                        # print(e)
                        pass
        driver.get('https://midway-auth.amazon.com')
        return driver

        
# Buyability checks
buyable_xp = '//*[@id="buyable"]'
searchable_xp = '//*[@id="searchable"]'
listing_xp = '//*[@id="listing_approved"]'
errors_xp = '//*[@class="alert alert-error"]'
warning_xp = '//*[@class="alert alert-notice"]'
record_xp = '//*[@id="has_item_record"]'
xref_xp = '//*[@id="has_xref"]'
offer_record_xp = '//*[@id="has_offer_record"]'
listing_price_entry_xp = '//*[@id="has_active_buy_listing"]'
mfn_availability_xp = '//*[@id="has_mfn_availability"]'
quantity_xp = '//*[@id="has_quantity"]'
blacklist_xp = '//*[@id="blacklist_record"]'
# seller_symptoms
fmid_xp = '//*[@id="fmid"]'
retail_xp = '//*[@id="is_retail"]'
#listing_symptoms
id_xp = '//*[@id="id"]'
type_xp = '//*[id="type"]'
has_price_xp = '//*[@id="has_price"]'
condition_xp = '//*[@id="condition"]'
subcondition_xp = '//*[@id="subcondition"]'
refusal_reason_codes_xp = '//*[@id="refusal_reason_codes"]'
listing_blocked_xp = '//*[@id="is_blocked"]'
blocks_xp = '//*[@id="blocks"]'
block_related_q_xp = '//*[@id="contact_for_block_related_questions"]'
why_block_palced_xp = '//*[@id="why_block_was_placed"]'
which_rule_xp = '//*[@id="block_placed_by_rule"]'
start_time_xp = '//*[@id="start_time"]'
listing_end_xp = '//*[@id="end_time"]'
listing_tombstoned_xp = '//*[@id="is_tombstoned"]'
is_seller_authorized_for_cat_xp = '//*[@id="is_seller_authorized_for_cat"]'
# Item - General Information
name_xp = '//*[@id="name"]'
gl_xp = '//*[@id="category"]'
product_type_xp = '//*[@id="product_type"]'
classification_xp = '//*[@id="item_classification"]'
creation_date_xp = '//*[@id="creation_time"]'
IMS_state_xp = '//*[@id="state"]'
merged_xp = '//*[@id="is_merged"]'
merged_to_xp = '//*[@id="merge_destination"]'
is_discontinued_xp = '//*[@id="is_discontinued"]'
discontinue_date_xp = '//*[@id="discontinue_date"]'
is_recalled_xp = '//*[@id="is_recalled"]'
recall_reason_xp = '//*[@id="recall_reason"]'
index_xp = '//*[@id="is_index_suppressed"]'
PCRP_restricted = '//*[@id="is_restricted"]'
restricted_reason = '//*[@id="restricted_reason"]'
display_website_xp = '//*[@id="is_surpressed"]'
surpressed_reasons_xp = '//*[@id="surpressed_reasons"]'
act_suppression_audit_info_xp = '//*[@id="act_suppression_audit_info"]'
child_xp = '//*[@id="is_shadow_child"]'
shadow_children_xp = '//*[@id="shadow_children"]'
SDP_Disabled_xp = '//*[@id="is_sdp_disabled"]'
launch_date_xp = '//*[@id="launch_date"]'
weight_xp = '//*[@id="shipping_weight"]'
# itemretail_symptoms
retail_contributions_xp = '//*[@id="marketplaces_with_retail_contributions"]'
num_retail_contributions_xp = '//*[@id="has_retail_contributions"]'
replenishment_category_xp = '//*[@id="replenishment_category"]'
active_xp = '//*[@id="is_retail_active"]'
# Item - Hazmat Information
hazmat_xp = '//*[@id="is_hazmat"]'
Shipping_Name_xp = '//*[@id="proper_shipping_name"]'
Regulatory_class_xp = '//*[@id="transport_regulatory_class"]'
Regulatory_id_xp = '//*[@id="united_nations_regulatory_id"]'
Regulatory_gp_xp = '//*[@id="regulatory_packing_group"]'
Hazmat_Exceptions_xp = '//*[@id="exceptions"]'
is_valid_transport_regulatory_class_xp = '//*[@id="is_valid_transport_regulatory_class"]'
under_review_xp = '//*[@id="under_review"]'
is_review_on_sla_xp = '//*[@id="is_review_on_sla"]'
compliance_approved_xp = '//*[@id="is_product_compliance_approved"]'
is_heavy_hazmat_xp = '//*[@id="is_heavy_hazmat"]'
# Item Recall Restricted Diagnostics
itemRestrictedReasonSymptom = '//*[@id="itemRestrictedReasonSymptom"]'
RuleActionSymptom = '//*[@id="RuleActionSymptom"]'
itemIsSuppressedSymptom = '//*[@id="itemIsSuppressedSymptom"]'
itemIsRecalledSymptom = '//*[@id="itemIsRecalledSymptom"]'
checkItemRecalledRestrictedError = '//*[@id="checkItemRecalledRestrictedError"]'
checkIsProhibitedPull = '//*[@id="checkIsProhibitedPull"]'
checkIsCopyright = '//*[@id="checkIsCopyright"]'
checkIsUpsteamProductSafetyControl = '//*[@id="checkIsUpsteamProductSafetyControl"]'
checkIsPrivateBrandsProactiveSuppression = '//*[@id="checkIsPrivateBrandsProactiveSuppression"]'
checkIsProductSafety = '//*[@id="checkIsProductSafety"]'
checkIsFoodSafety = '//*[@id="checkIsFoodSafety"]'
chooseRecallReinstateCTI = '//*[@id="chooseRecallReinstateCTI"]'
verifySteps = '//*[@id="verifySteps"]'
calculateCTI = '//*[@id="calculateCTI"]'
cutTicket = '//*[@id="cutTicket"]'
displayTicket = '//*[@id="displayTicket"]'
noTicket = '//*[@id="noTicket"]'
Enddiagnostic = '//*[@id="endDiagnostic"]'
# buyable_xp, searchable_xp, listing_xp, errors_xp, warning_xp

attributes = [record_xp, xref_xp, offer_record_xp, listing_price_entry_xp,
            mfn_availability_xp, quantity_xp, blacklist_xp, fmid_xp, retail_xp, id_xp, type_xp, has_price_xp, condition_xp, subcondition_xp,
            refusal_reason_codes_xp, listing_blocked_xp, blocks_xp, block_related_q_xp, why_block_palced_xp, which_rule_xp, start_time_xp,
            listing_end_xp, listing_tombstoned_xp, is_seller_authorized_for_cat_xp, name_xp, gl_xp, product_type_xp, classification_xp,
            creation_date_xp, IMS_state_xp, merged_xp, merged_to_xp, is_discontinued_xp, discontinue_date_xp, is_recalled_xp, recall_reason_xp,
            index_xp, PCRP_restricted, restricted_reason, display_website_xp, surpressed_reasons_xp, act_suppression_audit_info_xp, child_xp,
            shadow_children_xp, SDP_Disabled_xp, launch_date_xp, weight_xp, retail_contributions_xp, num_retail_contributions_xp,
            replenishment_category_xp, active_xp, hazmat_xp, Shipping_Name_xp, Regulatory_class_xp, Regulatory_id_xp, Regulatory_gp_xp,
            Hazmat_Exceptions_xp, is_valid_transport_regulatory_class_xp, under_review_xp, is_review_on_sla_xp, compliance_approved_xp,
            is_heavy_hazmat_xp, itemRestrictedReasonSymptom, RuleActionSymptom, itemIsSuppressedSymptom, itemIsRecalledSymptom,
            checkItemRecalledRestrictedError, checkIsProhibitedPull, checkIsCopyright, checkIsUpsteamProductSafetyControl,
            checkIsPrivateBrandsProactiveSuppression, checkIsProductSafety, checkIsFoodSafety, chooseRecallReinstateCTI, verifySteps,
            calculateCTI, cutTicket, displayTicket, noTicket, Enddiagnostic]

buyability = ['ASIN', 'Listing Buyable?', 'Item Searchable?', 'Is Listing approved?',
       'Errors', 'Warnings', 'Does this item have a record?',
       'Does this listing have a XREF entry?',
       'Does this listing have an offer record?',
       'Does this listing have a price entry?', 'has_mfn_availability',
       'Quantity (AFN/MFN)', 'blacklist_record',
       'What is/are this seller\'s FMID(s)?', 'Is Retail Merchant?', 'id',
       'has_price', 'condition', 'subcondition', 'refusal_reason_codes',
       'Is Listing blocked?', 'blocks',
       'Who to contact for block related questions?',
       'Why was the block placed?', 'Which rule placed block?', 'start_time',
       'Listing end date', 'Listing is tombstoned',
       'is_seller_authorized_for_cat']

general = ['Name', 'GL Product Group',
       'Product Type', 'Item Classification', 'Creation Date',
       'What is the item\'s IMS state?', 'Is item merged?',
       'What was the ASIN this symptom was merged to?', 'is_discontinued',
       'discontinue_date', 'is_recalled', 'recall_reason',
       'Is item suppressed from the index?', 'Is item PCRP restricted?',
       'restricted_reason', 'Is item suppressed from display on website?',
       'surpressed_reasons', 'act_suppression_audit_info',
       'Is this item a shadow child?', 'shadow_children', 'Is SDP Disabled?',
       'launch_date', 'Item shipping weight (pounds)',
       'Marketplaces with Amazon retail contributions',
       'Has Amazon retail contributions?', 'replenishment_category',
       'Is Retail active on the item (not marked as obsolete)?']

hazmat = ['Is item hazmat?', 'Proper Shipping Name',
       'Transportation Regulatory Class', 'United Nations Regulatory ID',
       'Regulatory Packing Group', 'Hazmat Exceptions',
       'is_valid_transport_regulatory_class', 'under_review',
       'is_review_on_sla', 'Is this item product compliance approved?',
       'is_heavy_hazmat']

recall = ['itemRestrictedReasonSymptom', 'RuleActionSymptom',
       'itemIsSuppressedSymptom', 'itemIsRecalledSymptom',
       'checkItemRecalledRestrictedError', 'checkIsProhibitedPull',
       'checkIsCopyright', 'checkIsUpsteamProductSafetyControl',
       'checkIsPrivateBrandsProactiveSuppression', 'checkIsProductSafety',
       'checkIsFoodSafety', 'chooseRecallReinstateCTI', 'verifySteps',
       'calculateCTI', 'cutTicket', 'displayTicket', 'noTicket',
       'End of diagnostic']


master_df = pd.DataFrame()
count = 0
def get_data(asin, seller, mp):
    global master_df, count, driver
    count += 1
    if count == 1:
         driver = mid_way_Authentication()
    child_df = pd.DataFrame()
    child_df['ASIN'] = [asin]
    driver.get(f'https://csi.amazon.com/tico/v3/?ts=tico&item_id={asin}&fn_sku=&customer_id={seller}&sku={asin}&marketplace_id={mp}&order_id=&filter=true&stage=prod&listing_type=purchasable&')
    def wait(xpath, number=10):
        global driver, wait_time
        wait_time = 0
        while True:
            sleep(1)
            wait_time += 1
            web_element = driver.find_elements(By.XPATH, xpath)
            if len(web_element) > 0:
                break
            if wait_time > number:
                print('TimeOut!, Unable to find the Xpath:', xpath)
                break
        return wait_time
    wait('//div[@class="well sidebar-nav"]', 60)
    if wait_time < 60:
        buyable = driver.find_element(By.XPATH, buyable_xp).text
        searchable = driver.find_element(By.XPATH, searchable_xp).text
        Listing_approved = driver.find_element(By.XPATH, listing_xp).text
        errors = driver.find_elements(By.XPATH, errors_xp)
        warns = driver.find_elements(By.XPATH, warning_xp)
        Errors = ''
        Warns = ''
        for error in errors:
            Errors = Errors + error.text + '\n'
        for warn in warns:
            Warns = Warns + warn.text + '\n'
        
        if 'ERRORS' in buyable:
            child_df['Listing Buyable?'] = ['No']
        else:
            child_df['Listing Buyable?'] = ['Yes']
        
        if 'ERRORS' in searchable:
            child_df['Item Searchable?'] = ['No']
        else:
            child_df['Item Searchable?'] = ['Yes']
        
        if 'ERRORS' in Listing_approved:
            child_df['Is Listing approved?'] = ['No']
        else:
            child_df['Is Listing approved?'] = ['Yes']
        child_df['Errors'] = [Errors]
        child_df['Warnings'] = [Warns]
        
        for attribute in attributes:
            try:
                attr = driver.find_element(By.XPATH, attribute).text
                attr = attr.split(':')
                child_df[attr[0].strip()] = [attr[1].strip()]
            except:
                pass
        # print(child_df)
        print('Data fetched for', asin, count)
    else:
         print('Unable to fetched data for', asin, count)
    master_df = pd.concat([master_df, child_df])

    Buyability = master_df[buyability]
    General = master_df[general]
    Hazmat = master_df[hazmat]
    Recall = master_df[recall]
    return master_df, Buyability, General, Hazmat, Recall
