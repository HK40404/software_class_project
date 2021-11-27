#  DOCKER

### DOCKER介绍

 https://zhuanlan.zhihu.com/p/187505981

### DOCKER基本教程

https://ruanyifeng.com/blog/2018/02/docker-tutorial.html

### DOCKER安装

参考官方文档https://docs.docker.com/engine/install/ubuntu/ 中的**Install using the repository**方法

### DOCKER更换国内仓库源

https://blog.csdn.net/weixin_44106306/article/details/115873140

### DOCKER向宿主机传文件

```shell
$ sudo docker cp 本地文件的路径 container_id:<docker容器内的路径>
```



### 项目打包迁移

1. 将容器打包为镜像：

    ```shell
    $ sudo docker commit -a "runoob.com" -m "my apache" <容器名称或id> <打包的镜像名称:标签>
    ```

    - -a :提交的镜像作者；
    - -c :使用Dockerfile指令来创建镜像；
    - -m :提交时的说明文字；

2. 将镜像导出

    ```shell
    #  将 something:latest镜像，导出到something-latest.tar
    $ sudo docker save -o ./something-latest.tar something:latest
    ```

3. 导入镜像

   ```shell
   $ docker load -i something-latest.tar
   ```

   
