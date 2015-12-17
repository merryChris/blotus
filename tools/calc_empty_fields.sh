#!/bin/bash

arr="link launch_time location logo_url introduction company_name artificial_person company_type shareholder_stucture registered_capital contributed_capital registered_address opening_date approved_date registration_authority business_licence institutional_framework tax_registration_num domain_name domain_date domain_company_type domain_company_name icp company_person_avatar_url company_person management_fee prepaid_fee cash_withdrawal_fee vip_fee transfer_fee mode_of_payment contact_address phone_400 phone fax email is_automatic_bid is_equitable_assignment trust_fund tender_security security_mode guarantee_institution business_type"

for x in ${arr[@]}; do
  echo ${x}, `cat wangjia_archive.log | grep "'${x}'" | grep Empty | wc -l`
done
