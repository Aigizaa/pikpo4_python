from processor.dataprocessor_service import DataProcessorService


"""
    Main-модуль, т.е. модуль запуска приложений ("точка входа" приложения)
"""


if __name__ == '__main__':
    service = DataProcessorService(datasource="murder_total_deaths.csv", db_connection_url="sqlite:///test1.db")
    service.run_service()
