FROM registry.cn-beijing.aliyuncs.com/modelscope-repo/modelscope:ubuntu20.04-cuda11.3.0-py38-torch1.11.0-tf1.15.5-1.8.0 as dev-base
RUN rm /usr/lib/x86_64-linux-gnu/libnvidia-*
RUN rm /usr/lib/x86_64-linux-gnu/libcuda.so*
RUN pip install gradio
RUN pip install pymongo
RUN pip install redis
COPY . /zhuan_gao6
WORKDIR /zhuan_gao6
EXPOSE 7776
EXPOSE 8888
CMD /zhuan_gao6/startup.sh


