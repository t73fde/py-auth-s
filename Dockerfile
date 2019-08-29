# Basis-Image
FROM hshnwinps/wsgi
COPY app.tgz  /
RUN cd /usr/src \
 && tar xfz /app.tgz \
 && rm /app.tgz \
 && chown -R nobody:nobody .

USER nobody

CMD ["gunicorn", \
  "-b", "0.0.0.0:9876", "--chdir", "/usr/src", \
  "-w", "3", \
  "--error-logfile", "-", "--capture-output", \
  "py_auth_s.webapp"]
