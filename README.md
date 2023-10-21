### Project setup

- Clone the project `git clone https://github.com/DanSantoDomingo/django-loans.git`
- Run `cd django-loans`
- Run `docker-compose up`
- Goto `http://127.0.0.1:8000/api/docs/swagger-ui/`


### Uploading the excel file

- Goto `http://127.0.0.1:8000/api/docs/swagger-ui/#/loans-excel/loansExcelCreate`
- Click the button `Try it out`
- Choose `multipart/form-data` in the dropdown
- Upload the excel file by clicking the `Choose File` button then click `Execute`


### Viewing the Loan Amortization Schedule
- Goto `http://127.0.0.1:8000/api/docs/swagger-ui/#/amortization-schedules/amortizationSchedulesList`
- Enter the loan number from the excel file you uploaded then click `Execute`


