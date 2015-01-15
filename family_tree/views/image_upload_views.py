# encoding: utf-8

import os
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
import json



MAX_FILE_SIZE = 15000000  # bytes


def get_file_size(file):
    file.seek(0, 2)  # Seek to the end of the file
    size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return size


#https://blueimp.github.io/jQuery-File-Upload/basic-plus.html
@login_required
def edit_profile_photo(request, person_id):
    '''
    That shows the upload form
    '''
    person = get_object_or_404(Person, id = person_id)

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404


    template = loader.get_template('family_tree/image_upload.html')
    context = RequestContext(request,{
                                    'person' : person,
                                })

    response = template.render(context)
    return HttpResponse(response)


@login_required
def image_upload(request, person_id):
    '''
    View that receives the uploaded image
    '''

    person = get_object_or_404(Person, id = person_id)

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404


    uploaded = request.FILES['picture']

    #get the name, and extension and create a unique filename
    name, ext = os.path.splitext(uploaded.name)
    filename =  str(uuid.uuid4()) +'.jpg'
    photo_file = ''.join([settings.MEDIA_ROOT, 'profile_photos/', filename])

    result = {
        'name': uploaded.name,
        'size': uploaded.size,
        'url': '/media/profile_photos/' + filename,
        'filename': filename ,
    }

    if uploaded.size > MAX_FILE_SIZE:
        result['error'] = _('File is too big')
        return HttpResponse(json.dumps(result), content_type='application/json')

    #Write the file to the destination
    destination = open(photo_file, 'wb+')

    for chunk in uploaded.chunks():
        destination.write(chunk)
    destination.close()

    #Check this is a valid image
    try:
        person.set_hires_photo(filename)

    except Exception as ex:
        result['error'] = str(ex)
        return HttpResponse(json.dumps(result), content_type='application/json')

    person.save()

    return HttpResponse(json.dumps(result), content_type='application/json')



@login_required
def image_resize(request, person_id):
    '''
    Shows the image resize page
    '''
    person = get_object_or_404(Person, id = person_id)

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404

    #Ensure that profile is not locked
    if request.user.id != person.user_id and person.locked == True:
        raise Http404


    template = loader.get_template('family_tree/image_resize.html')
    context = RequestContext(request,{
                                    'person' : person,
                                })

    response = template.render(context)
    return HttpResponse(response)

