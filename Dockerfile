# Basis-Image
FROM hshnwinps/wsgi
COPY py_auth_s.py /usr/src
RUN chown -R nobody:nobody /usr/src

USER nobody

CMD ["gunicorn", \
  "-b", "0.0.0.0:9876", "--chdir", "/usr/src", \
  "-w", "3", \
  "--error-logfile", "-", "--capture-output", \
  "py_auth_s"]
