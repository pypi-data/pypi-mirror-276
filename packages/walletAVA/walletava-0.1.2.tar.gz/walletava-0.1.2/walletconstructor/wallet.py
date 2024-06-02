from walletconstructor.security import Security
from web3 import Web3
from web3.exceptions import ProviderConnectionError, TransactionNotFound, InvalidAddress, Web3ValidationError, ContractLogicError, Web3Exception
from walletconstructor.transaction.wallet import TransactionHistory
from walletconstructor.utils.wallet import WalletUtils
from walletconstructor.infos.infos import Infos
from decimal import Decimal
from typing  import Dict, Literal, Any
class Wallet:
    def __init__(
            self,
            security_wallet:Security,
            http_provider:str
            ) -> None:
        self.security = security_wallet
        self._http_provider = http_provider
        self.web3 = None
        self.transactions = None
        self.infos = None
        self.__connect()

    def __connect(self) -> None:
        try:
            self.web3 = Web3(Web3.HTTPProvider(self._http_provider))
            if not self.web3.is_connected():
                raise ProviderConnectionError("No Provider Valid")
            self.transactions = TransactionHistory(self.web3)
            self.infos = Infos(self.web3, self.security)
        except(ProviderConnectionError, Web3Exception, Exception) as e:
            raise ProviderConnectionError("Error Provider") from e
        
    def send(
            self, 
            to: str, 
            value: Decimal, 
            speed: Literal['fast', 'average', 'slow'] = 'fast'
        ) -> Dict[str, Any]:
        try:
            assert self.web3.is_address(to), InvalidAddress("Invalid Address")
            res = WalletUtils.build_transaction(
                self.web3,
                self.security,
                to,
                value,
                speed
            )
            self.transactions._wait_transaction(res)
            self.infos.update_infos()
            return {
                'build_transaction': res['build_transaction'],
                'speed': speed,
                'transaction_receipt': self.transactions.history[res['hash_transaction']]
            }
        except (TransactionNotFound, InvalidAddress, Web3ValidationError, ContractLogicError, Web3Exception) as e:
            raise Exception("Erreur lors de l'envoi de la transaction") from e
        
    def verify_addr(self, addr: str, raise_exception: bool = False) -> bool:
        try:
            if Web3.is_address(addr):
                return True
            if raise_exception:
                raise InvalidAddress("Address Invalide")
            else:
                return False
        except (Web3Exception, Exception) as e:
            raise Exception("Erreur lors de la vérification de l'adresse") from e
        
    def balance(self) -> Decimal:
        try:
            value_wei = self.web3.eth.get_balance(self.security.addr_ethereum)
            return self.web3.from_wei(value_wei, 'ether')
        except (Web3Exception, Exception) as e:
            raise Exception("Error balance") from e