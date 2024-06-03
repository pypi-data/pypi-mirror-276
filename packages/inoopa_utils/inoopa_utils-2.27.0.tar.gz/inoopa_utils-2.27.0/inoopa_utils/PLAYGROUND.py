from custom_types.companies import Address


company_dict = {"address": None}
address=Address(**company_dict['address']) if company_dict and company_dict.get('address')
print("adr: ", address)