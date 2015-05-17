from django import template

register = template.Library()


# @register.inclusion_tag('base/templatetags/render_get_parameters.html')
# def render_get_parameters(request, *exclude_parameters):
#     """
#     :param request: http request
#     :param exclude_parameter: get parameter to be excluded from get parameters in request
#     :return: template with get parameters rendered as hidden inputs
#     """
#     parameters = request.GET.copy()
#     if exclude_parameters:
#         for exclude_parameter in exclude_parameters:
#             parameters.pop(exclude_parameter, None)
#     return {'parameters': parameters}