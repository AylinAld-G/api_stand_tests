import sender_stand_request
import data


def get_user_body(first_name):
    current_body=data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

#Función de prueba positiva
def positive_assert(first_name):
    #La versión actualizada del cuerpo de solicitud que contiene "Aa" se guarda en "user_body"
    user_body=get_user_body(first_name)
    #El resultado de la solicitud relevante se guarda en la variable "user_response"
    user_response=sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    #El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en "users_table_response"
    users_table_response=sender_stand_request.get_users_table()
    #El string que debe estar en el cuerpo de la respuesta para recibir datos de la tabla "users" se ve así
    str_user=user_body["firstName"] + "," + user_body["phone"] + "," \
    +user_body["address"] + ",,," + user_response.json()["authToken"]

    #Comprueba si el usuario existe y es único/a
    assert users_table_response.text.count(str_user) == 1

#Prueba 1: Creación de usuario
#El parámetro "firstName" contiene 2 caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


#Prueba 2: "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("AndreaEmirethJo")

#Función negative_assert_symbol()
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == ("Nombre de usuario o usuaria incorrecto. \
                                               El nombre solo puede contener letras latinas y la longitud debe ser \
                                               de 2 a 15 caracteres")

#Prueba 3: "firstName" contiene una letra
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


#Prueba 4: "firstName" contiene 16 letras
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

#Prueba 5: espacio en "firstName"
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")

#Prueba 6: "firstName" contiene caracter especial
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("N%@")

#Prueba 7: "firstName" contiene un número
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

#Pruebas 8 y 9: Preparación: FUNCIÓN NEGATIVE_ASSERT_NO_FIRST_NAME
def negative_assert_no_first_name(user_body):
    response=sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se enviaron todos los parámetros necesarios"

#Prueba 8: Error. La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    #El diccionario con el cuerpo de la solicitud se copia del archivo data a "user_body"
    #De lo contrario se podrían perder los datos del diccionario de origen
    user_body = data.user_body.copy()
    #El parámetro firstName se elimina de la solicitud
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

#Prueba 9: El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)


#Prueba 10: "firstName" se pasa con valor tipo number
def test_create_user_number_type_first_name_get_error_response():
    user_body= get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400  #va a devolver 500, pero ntp by now