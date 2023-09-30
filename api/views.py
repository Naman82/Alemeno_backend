from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import JsonResponse
import numpy as np
import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

class PhotoProcessView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def extract_colors( self, file_path: str):
        image = Image.open(file_path)
        image_array = np.array(image)
        num_pixels = image_array.shape[0] * image_array.shape[1]
        image_array_reshaped = image_array.reshape(num_pixels, -1)
        num_colors = 10
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(image_array_reshaped)
        colors = kmeans.cluster_centers_
        colors = colors.astype(int)
        result = []
        for color in colors:
            result.append(color.tolist())
        return result

    def post(self, request):
        try:
            photo = request.data.get('image')
            
            if not photo:
                return JsonResponse({'error': 'No image data provided'}, status=400)

            temp_image_path = 'temp_image.jpg'
            with open(temp_image_path, 'wb') as temp_img_file:
                for chunk in photo.chunks():
                    temp_img_file.write(chunk)

            colors = self.extract_colors(temp_image_path)

            os.remove(temp_image_path)

            result_json = {
                'URO': colors[0], 'BIL': colors[1], 'KET': colors[2], 'BLD': colors[3], 'PRO': colors[4], 'NIT': colors[5], 'LEU': colors[6], 'GLU': colors[7], 'SG': colors[8], 'PH': colors[9]
            }
            
            return JsonResponse(result_json, safe=False)

        except Exception as e:
            return JsonResponse(str(e), safe=False)
