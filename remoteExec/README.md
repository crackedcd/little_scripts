# 这个脚本用于批量在远程服务器上执行命令
> 脚本依赖python3.x, 依赖Crypto和ecdsa模块, 依赖paramiko.


-------------------------------------------
# 执行方法

## 直接执行命令
> 定义命令, 该工具会将命令批量下发到各机器执行
> ```python
>     exec_cmds(ips_list, cmds_list)
> ```

## 执行一个写好的脚本
> 编写好一个脚本, 该工具会将脚本批量下发, 然后执行脚本
> ```python
>     exec_files(ips_list, bash_file)
> ```

## 执行一个写好的脚本
> 推荐使用./run.sh执行, 推送xxx_script.sh脚本, 会有log记录
> ```python
>     ./run.sh
> ```

## 执行方式
> 
- 顺序执行
- 多进程同时执行
- 多线程同时执行(可能造成显示错误)
- 协程


# 备注
> 依赖getpasswd脚本取得机器密码
